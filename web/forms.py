from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.core.exceptions import ValidationError
from interface.oracleDB import *
import re

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

    def __init__(self, db_pool, id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addToolForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.db_pool = db_pool
        self.id = id

        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_manufacturer(self):
        return self.cleaned_data['manufacturer'].strip()

    def clean_model_name(self):
        return self.cleaned_data['model_name'].strip()

    def clean_serial_number(self):
        data = self.cleaned_data['serial_number'].strip()
        if serial_number_in_use(self.db_pool, self.id, data):
            raise ValidationError('Serial number already exists')

        return data

class AddBuildingForm(forms.Form):
    address = forms.CharField(
        label='Address',
        max_length=45,
        required=True
    )
    city = forms.CharField(
        label='City',
        max_length=45,
        required=True
    )
    zipcode = forms.CharField(
        label='Zipcode',
        max_length=45,
        required=True
    )

    def __init__(self, action = 'add', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addBuildingForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = action + '/building'

        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_address(self):
        return self.cleaned_data['address'].strip()

    def clean_city(self):
        return self.cleaned_data['city'].strip()

    def clean_zipcode(self):
        return self.cleaned_data['zipcode'].strip()

class AddDepartmentForm(forms.Form):
    department_name = forms.CharField(
        label='Department Name',
        max_length=45,
        required=True
    )
    website = forms.CharField(
        label='Website',
        max_length=45,
        required=False
    )

    def __init__(self, db_pool, deptid = -1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addDepartmentForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

        choices = []
        with get_buildings_no_dept(db_pool, deptid) as csr:
            for id, address, city, zipcode in csr:
                choices.append((id, '%s %s %s' % (address, city, zipcode)))
        self.fields['building'] = forms.TypedChoiceField(
            label='Building',
            choices = tuple(choices),
            required=True,
            widget=forms.Select(attrs={'size' : 5})
        )

    def clean_department_name(self):
        return self.cleaned_data['department_name'].strip()

    def clean_website(self):
        data = self.cleaned_data['website'].strip()
        if not data:
            return data

        res = re.search(r"(https?:\/\/)|(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}", data)

        if not res:
            raise ValidationError('Not a valid website')

        return data
        
class AddResearcherForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=45,
        required=True
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=45,
        required=True
    )
    email = forms.EmailField(
        label='Email Address',
        max_length=45,
        required=True
    )
    phone = forms.CharField(
        label='Phone number',
        max_length=45,
        required=True
    )

    def __init__(self, db_pool, id = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-addResearcherForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

        self.db_pool = db_pool
        self.id = id

        choices = []
        with get_departments(db_pool) as csr:
            for id, name, _, _ in csr:
                choices.append((id, name))

        self.fields['department'] = forms.TypedChoiceField(
            label='Department',
            choices = tuple(choices),
            required=True,
            widget=forms.Select(attrs={'size' : 5})
        )

        self.fields['role'] = forms.TypedChoiceField(
            label='Role',
            choices = (('tehnician', 'tehnician'), ('laborant', 'laborant'), ('cercetator', 'cercetator')),
            required=True,
            widget=forms.Select(attrs={'size' : 3})
        )

    def clean_first_name(self):
        data = self.cleaned_data['first_name'].strip()
        if not data.replace(' ', '').isalpha():
            raise ValidationError('Invalid character detected')

        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name'].strip()
        if not data.replace(' ', '').isalpha():
            raise ValidationError('Invalid character detected')

        return data

    def clean_email(self):
        data = self.cleaned_data['email'].strip()

        if email_in_use(self.db_pool, self.id, data):
            raise ValidationError('Email already in use')

        return data

    def clean_phone(self):
        data = self.cleaned_data['phone'].strip()
        res = re.search(r"((\+4)*[0-9]{10})|((\+4)*0(\([0-9]{3}\))[0-9]{6})", data)

        if not res:
            raise ValidationError('Not a valid phone number')

        if phone_in_use(self.db_pool, self.id, data):
            raise ValidationError('Phone number already in use')

        return data
    

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

        choices = []
        with get_users(db_pool) as csr:
            for id, fname, lname, dept, _, _, role in csr:
                choices.append((id, "%s %s %s at %s" % (fname, lname, role, dept)))

        self.fields['researchers'] = forms.TypedMultipleChoiceField(
            label='Researchers',
            choices = tuple(choices),
            required=True,
            widget=forms.SelectMultiple(attrs={'size' : 20})
        )

        choices= []
        with get_tools(db_pool) as csr:
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
        self.helper.form_id = 'id-addResultForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        choices = []
        with get_experiments(db_pool) as csr:
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
