from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)

    class Meta:
        model = User                           # use our custom user 
        fields = ['username', 'email', 'phone', 'password1', 'password2']



def clean_phone(self):                         # automatically call when we call is_valid()  
    phone = self.cleaned_data.get('phone')
    if phone and not phone.startswith('09'):   # فقط اگه چیزی وارد شده بود چک کن
        raise forms.ValidationError('شماره تلفن باید با 09 شروع بشه')
    return phone



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }




