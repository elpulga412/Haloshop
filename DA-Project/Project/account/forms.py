from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    re_password = forms.CharField(required=True, widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'address']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'w3-input w3-border w3-lightgray', 'name':'field', 'onfocus':"this.value=''"})


    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError("Email đã được đăng ký")
        return email

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")
        if password != re_password:
            raise ValidationError("Mật khẩu sai! Nhập lại mật khẩu")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'w3-border w3-lightgray', 'name':'field'})