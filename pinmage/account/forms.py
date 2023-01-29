from django.contrib.auth.models import User
from .models import Profile
from django import forms


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        data = self.cleaned_data['username']
        qs = User.objects.exclude(id=self.instance.id).filter(username=data)
        if qs.exists():
            raise forms.ValidationError("Username already in use!")
        return data

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']