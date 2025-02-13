from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name","mobile","email","aadhar","father",
        "dob","gender","state","photo"]
      