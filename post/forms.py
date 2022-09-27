from django import forms
from django.contrib.auth.models import User


class UserRrgisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Retype Password", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', "email", "password2")
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder":"First Name", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}),
            'last_name': forms.TextInput(attrs={"placeholder":"Last Name", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}),
            'email': forms.EmailInput(attrs={"placeholder":"Email", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}),
            'username': forms.TextInput(attrs={"placeholder":"Username", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}),
            'password': forms.PasswordInput(attrs={"placeholder":"password", "class":"w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"}),
        }
        help_texts = {
            'password2' : ('Retype your password')
        }
    def clean(self):
        cleaned_data = super(UserRrgisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError(
                "password arent match"
            )


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length = 150, widget=forms.TextInput(attrs={"class":"w-full border-none bg-transparent outline-none placeholder:italic focus:outline-none", "placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "w-full border-none bg-transparent outline-none placeholder:italic focus:outline-none", "placeholder":"Password"}))