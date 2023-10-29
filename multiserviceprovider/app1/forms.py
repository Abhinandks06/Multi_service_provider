from django import forms
from .models import MyUser
# client details
class ClientProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username', 'dob']  # Include 'dob' in the fields list
        