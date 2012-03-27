from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit

from .models import Log


class LogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('title', css_class='span8'),
            Field('text', css_class='span8', rows=10)
        )

        helper.add_input(Submit('submit', 'Upload Log',
                                css_class='btn-primary'))

        self.helper = helper

        super(LogForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Log
        exclude = ['slug', 'submitter']
