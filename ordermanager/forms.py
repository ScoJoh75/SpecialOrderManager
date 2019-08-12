from django import forms
from ordermanager.models import Order, Contact


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('author', 'order_number', 'order_reason', 'customer', 'product_name', 'title', 'design_code',
                  'carrier', 'ship_date', 'process_date', 'sequence_numbers', 'tooling_status', 'programming_status',
                  'engineering_framing_setup', 'engineering_panel_setup', 'engineering_lipping_setup',
                  'engineering_assembly', 'engineering_options', 'engineering_other', 'order_notes', 'feedback', 'date')

        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'textinputclass'}),
            'order_reason': forms.Select(attrs={'class': 'comboinputclass'}),
            'customer': forms.Select(attrs={'class': 'comboinputclass'}),
            'product_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'design_code': forms.TextInput(attrs={'class': 'textinputclass'}),
            'carrier': forms.Select(attrs={'class': 'comboinputclass'}),
            'ship_date': forms.DateInput(attrs={'class': 'dateinputclass'}),
            'process_date': forms.DateInput(attrs={'class': 'dateinputclass'}),
            'sequence_numbers': forms.TextInput(attrs={'class': 'textinputclass'}),
            'tooling_status': forms.Select(attrs={'class': 'comboinputclass'}),
            'programming_status': forms.CheckboxInput(),
            'engineering_framing_setup': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'engineering_panel_setup': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'engineering_assembly': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'engineering_lipping_setup': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'engineering_options': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'engineering_other': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'}),
            'order_notes': forms.Textarea(attrs={'class': 'textinputareaclass'}),
            'feedback': forms.Textarea(attrs={'class': 'textinputareaclass'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email_address', 'site', 'active')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'last_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'email_address': forms.EmailInput(attrs={'class': 'textinputclass'}),
            'site': forms.Select(attrs={'class': 'comboinputclass'}),
            'active': forms.CheckboxInput(attrs={'class': 'checkboxinputclass'})
        }
