from django import forms
from django.contrib.auth.models import User

from .models import Stat
from .models import LS_HOMELANDS, DS_HOMELANDS, SS_HOMELANDS


class SubmitStatForm(forms.ModelForm):

    apikey = forms.CharField(max_length=38)

    strength = forms.IntegerField(min_value=3, max_value=21)
    intel = forms.IntegerField(min_value=3, max_value=19)
    wil = forms.IntegerField(min_value=3, max_value=19)
    dex = forms.IntegerField(min_value=3, max_value=19)
    con = forms.IntegerField(min_value=3, max_value=19)

    def clean(self):
        data = self.cleaned_data

        klass = data.get('klass', None)
        faction = data.get('faction', None)
        homeland = data.get('homeland', None)

        # If the klass is C then the faction must be H
        if klass == 'C' and faction != 'H':
            raise forms.ValidationError("Only humans can be channelers.")

        # Make sure the faction and homeland are valid together
        hls = {'H': LS_HOMELANDS, 'D': DS_HOMELANDS, 'S': SS_HOMELANDS}[faction]

        hls = map(lambda r: r[0], hls)

        if homeland not in hls:
            raise forms.ValidationError("Homeland '%s' is not valid for this faction.")

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
