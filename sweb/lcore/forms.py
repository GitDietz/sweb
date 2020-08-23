from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    full_name = forms.CharField(label= "Your name and surname", required=True)
    email = forms.EmailField(required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 40}), required=True)

    class Meta:
        fields = ['full_name', 'email', 'content']
