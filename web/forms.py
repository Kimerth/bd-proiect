from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from interface.oracleDB import *

class AddToolForm(forms.Form):
    manufacturer = forms.CharField(
        label='Manufacturer',
        max_length=45,
        required=True
    )
    model_name = forms.CharField(
        label='Model Name',
        max_length=45,
        required=True
    )
    serial_number = forms.CharField(
        label='Serial Number',
        max_length=45,
        required=True
    )
    specifications = forms.CharField(
        label='Specifications',
        max_length=1024,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addToolForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

class AddExperimentForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=256,
        required=True
    )
    description = forms.CharField(
        label='Description',
        max_length=2048,
        required=True
    )
    theory = forms.CharField(
        label='Theory',
        max_length=2048,
        required=True
    )

    def __init__(self, db_pool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addExperimentForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

        csr = get_users(db_pool)
        choices = []
        for id, fname, lname, dept, _, _, role in csr:
            choices.append((id, "%s %s %s at %s" % (fname, lname, role, dept)))

        self.fields['researchers'] = forms.TypedMultipleChoiceField(
            label='Researchers',
            choices = tuple(choices),
            required=True,
            widget=forms.SelectMultiple(attrs={'size' : 20})
        )

        csr = get_tools(db_pool)
        choices= []
        for id, manufacturer, mname, _, _ in csr:
            choices.append((id, "%s %s" % (manufacturer, mname)))

        self.fields['tools'] = forms.TypedMultipleChoiceField(
            label='Tools',
            choices = tuple(choices),
            required=True,
            widget=forms.SelectMultiple(attrs={'size' : 10})
        )

class AddResultForm(forms.Form):
    remarks = forms.CharField(
        label='Remarks',
        max_length=4000,
        required=True
    )

    observations = forms.CharField(
        label='Observations',
        max_length=4000,
        required=True
    )

    description = forms.CharField(
        label='Description',
        max_length=4000,
        required=True
    )

    def __init__(self, db_pool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addToolForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        csr = get_experiments(db_pool)
        choices = []
        for id, title, _, _ in csr:
            choices.append((id, title))

        self.fields['experiment'] = forms.TypedChoiceField(
            label='Experiment',
            choices = tuple(choices),
            required=True,
            widget=forms.Select(attrs={'size' : 10})
        )

        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'experiment',
                'remarks',
                'observations',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )
