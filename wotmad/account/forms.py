from django import forms
from django.contrib.auth.models import User


class AccountSetupForm(forms.Form):
    username = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        super(AccountSetupForm, self).__init__(*args, **kwargs)

        self._user = user

    def clean_username(self):
        clean = self.cleaned_data['username']

        existing = User.objects.filter(username=clean)
        existing = existing.exclude(pk=self._user.pk)

        if existing.count():
            raise forms.ValidationError("That username is already taken.")

        return clean
