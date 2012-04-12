from django import forms
from django.contrib.auth.models import User

from .models import Stat


class SubmitStatForm(forms.ModelForm):

    apikey = forms.CharField(max_length=38)

    hitpoints = forms.IntegerField(min_value=20, max_value=200)
    moves = forms.IntegerField(min_value=100, max_value=200)
    spellpoints = forms.IntegerField(min_value=0, max_value=200,
                                     required=False)

    strength = forms.IntegerField(min_value=3, max_value=21)
    intel = forms.IntegerField(min_value=3, max_value=19)
    wil = forms.IntegerField(min_value=3, max_value=19)
    dex = forms.IntegerField(min_value=3, max_value=19)
    con = forms.IntegerField(min_value=3, max_value=19)

    def clean(self):
        data = self.cleaned_data

        klass = data.get('klass', None)
        faction = data.get('faction', None)
        spellpoints = data.get('spellpoints', None)

        # If the klass is C then the faction must be H
        if klass == 'C' and faction != 'H':
            raise forms.ValidationError("Only humans can be channelers.")

        # If the klass is C then they must send spellpoints greater than 0
        if klass == 'C' and spellpoints <= 0:
            raise forms.ValidationError("Invalid spell points.")

        return data

    def clean_apikey(self):
        # Ensure they submit a valid api key
        clean = self.cleaned_data.get('apikey')

        # Try to find a user with this API key
        try:
            user = User.objects.get(apikey__key=clean, is_active=True)
            self.user = user
        except User.DoesNotExist:
            self.user = None
            raise forms.ValidationError("Invalid API key.")

        return clean

    class Meta:
        model = Stat
        exclude = ['submitter', 'date_submitted']
