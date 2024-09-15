from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Pet, PetImage
from .forms import PetForm, PetImageForm

def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'pets/pet_list.html', {'pets': pets})

def add_pet(request):
    if request.method == 'POST':
        pet_form = PetForm(request.POST)
        if pet_form.is_valid():
            pet = pet_form.save()
            
            new_images = request.FILES.getlist('new_image')
            new_captions = request.POST.getlist('new_caption')
            
            for image, caption in zip(new_images, new_captions):
                PetImage.objects.create(pet=pet, image=image, caption=caption)

            messages.success(request, 'Pet added successfully!')
            return redirect('pets:pet_list')
    else:
        pet_form = PetForm()
        image_form = PetImageForm()

    return render(request, 'pets/add_pet.html', {'pet_form': pet_form, 'image_form': image_form})

def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)

    if request.method == 'POST':
        pet_form = PetForm(request.POST, instance=pet)
        if pet_form.is_valid():
            pet = pet_form.save()
            
            # Update existing image captions
            for image in pet.images.all():
                caption_key = f'existing_caption_{image.id}'
                if caption_key in request.POST:
                    image.caption = request.POST[caption_key]
                    image.save()
            
            # Add new images
            new_images = request.FILES.getlist('new_image')
            new_captions = request.POST.getlist('new_caption')
            
            for image, caption in zip(new_images, new_captions):
                if image:  # Only create a new PetImage if an image file was uploaded
                    PetImage.objects.create(pet=pet, image=image, caption=caption)

            messages.success(request, 'Pet updated successfully!')
            return JsonResponse({'status': 'success', 'message': 'Pet updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': pet_form.errors}, status=400)
    else:
        pet_form = PetForm(instance=pet)
        image_form = PetImageForm()

    pet_images = pet.images.all()
    
    return render(request, 'pets/edit_pet.html', {
        'pet': pet,
        'pet_form': pet_form, 
        'image_form': image_form, 
        'pet_images': pet_images
    })

@require_POST
@csrf_exempt
def delete_pet_image(request, image_id):
    image = get_object_or_404(PetImage, pk=image_id)
    pet_id = image.pet.id
    image.delete()
    
    return JsonResponse({'status': 'success', 'message': 'Image deleted successfully!'})

@require_POST
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    pet.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Pet deleted successfully!'})
    else:
        messages.success(request, 'Pet deleted successfully!')
        return redirect('pets:pet_list')

def get_pet_images(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    images = pet.images.all()
    image_data = [
        {
            'id': image.id,
            'url': image.image.url,
            'caption': image.caption,
            'filename': image.image.name.split('/')[-1]
        } for image in images
    ]
    return JsonResponse(image_data, safe=False)