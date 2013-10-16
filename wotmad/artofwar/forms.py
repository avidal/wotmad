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
            Field('pov', css_class='span8 select2', data_placeholder='Select...'),
            Field('categories', css_class='span8 select2', data_placeholder='Select...'),
            Field('description', css_class='span8', rows=3),
            Field('text', css_class='span8', rows=10)
        )

        helper.add_input(Submit('submit', 'Upload Log',
                                css_class='btn-primary'))

        self.helper = helper

        super(LogForm, self).__init__(*args, **kwargs)
        self.fields['categories'].help_text = ''

    class Meta:
        model = Log
        exclude = ['slug', 'submitter']
