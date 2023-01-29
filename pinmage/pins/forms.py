from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Pin
from django import forms
import requests

class PinCreateForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description', 'tags', 'pin']






