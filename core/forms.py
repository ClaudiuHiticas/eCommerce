from django import forms

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('R', 'Ramburs')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nume',
        'id': 'first_name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Prenume',
        'id': 'last_name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'id': 'email'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Numar telefon',
        'id': 'phone'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Adresa',
        'id': 'address'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Oras',
        'id': 'city'
    }))
    county = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Judet',
        'id': 'county'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
