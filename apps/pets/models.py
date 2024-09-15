from django.db import models
from django.utils.text import slugify
import os

def pet_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a slug from the pet's name
    slug = slugify(instance.pet.name)
    # Return the new file path
    return f'pet_images/{slug}/{slug}_{instance.id}.{ext}'

class Pet(models.Model):
    SIZE_CHOICES = [
        ('Toy', 'Toy'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Giant', 'Giant'),
    ]

    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='Medium')

    def __str__(self):
        return self.name
    
class PetImage(models.Model):
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pet_image_path)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.name} - Image"

    def filename(self):
        return os.path.basename(self.image.name)