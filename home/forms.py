# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Doctor,Patient
from . import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Doctor
import re

# Forms
class DoctorUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Password must be at least 8 characters long and include both letters and numbers."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address is already registered.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one letter.')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.')
        return password


class DoctorForm(forms.ModelForm):
    mobile = forms.CharField(
        help_text="Mobile number must be exactly 10 digits."
    )

    class Meta:
        model = Doctor
        fields = ['profile_pic', 'address', 'mobile', 'status','department', 'experience']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one letter.')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.')
        return password

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError('Mobile number must be exactly 10 digits.')
        return mobile

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address.strip():
            raise ValidationError('Address cannot be empty.')
        return address


# class DoctorUserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']

# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         fields = ['profile_pic', 'address', 'mobile', 'department', 'experience']




# #for teacher related form
# class PatientUserForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(),
#         help_text="Password must be at least 8 characters long and include both letters and numbers."
#     )
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
        
# class PatientForm(forms.ModelForm):
#     assignedDoctorId = forms.ModelChoiceField(
#         queryset=Doctor.objects.all().filter(status=True),
#         empty_label="Name and Department",
#         to_field_name="id"  # Change from "user_id" to "id" to ensure the correct reference
#     )
    
#     class Meta:
#         model = Patient
#         fields = ['address', 'mobile', 'status', 'symptoms', 'profile_pic']



from django.core.exceptions import ValidationError
import re

from django import forms
from django.core.exceptions import ValidationError
import re
from django import forms
from django.core.exceptions import ValidationError
import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Patient, Doctor
import re


class PatientUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Password must be at least 8 characters long and include both letters and numbers."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        return password


class PatientForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.all().filter(status=True),
        empty_label="Name and Department",
        to_field_name="id",
        required=True
    )

    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'status', 'symptoms', 'profile_pic']
        widgets = {
            'address': forms.Textarea(attrs={'required': True}),
            'mobile': forms.TextInput(attrs={'required': True}),
            'symptoms': forms.Textarea(attrs={'required': True}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError("Mobile number must contain exactly 10 digits.")
        return mobile

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address.strip():
            raise ValidationError("Address cannot be empty.")
        return address

    def clean_symptoms(self):
        symptoms = self.cleaned_data.get('symptoms')
        if not symptoms.strip():
            raise ValidationError("Symptoms field cannot be empty.")
        return symptoms

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic and not profile_pic.content_type.startswith('image/'):
            raise ValidationError("Profile picture must be a valid image file.")
        return profile_pic
