from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit

from .models import Script


class ScriptForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('title', css_class='span8'),
            Field('description', css_class='span8', rows=3),
            Field('source', css_class='span8', rows=10)
        )

        helper.add_input(Submit('submit', 'Upload Script',
                                css_class='btn-primary'))

        self.helper = helper

        super(ScriptForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Script
        exclude = ['slug', 'submitter']
