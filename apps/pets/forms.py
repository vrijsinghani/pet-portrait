from django import forms
from .models import Pet, PetImage

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'size']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pet name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pet breed'}),
            'size': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select pet size'}),
        }

class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter image caption'}),
        }