from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,Product

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, age=self.cleaned_data['age'])
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'available_quantity']