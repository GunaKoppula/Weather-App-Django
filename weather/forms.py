from django import forms
from django.contrib.auth.models import User

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
#     username = forms.CharField(max_length=150, required=True)
    
#     def clean_username(self):
#         username = self.cleaned_data.get('username')

#         # Check for allowed characters
#         if not re.match(r'^[\w@.+-]*$', username):
#             raise ValidationError("Only letters, digits, and @/./+/-/_ are allowed.")

#         if len(username) > 150:
#             raise ValidationError("Username must be 150 characters or fewer.")

#         return username
