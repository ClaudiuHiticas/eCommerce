from django import forms

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nume'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Prenume'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Numar telefon'
    }))
    adress = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Adresa'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Oras'
    }))
    county = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Judet'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
