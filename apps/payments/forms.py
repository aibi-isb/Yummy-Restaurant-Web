from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from apps.core.choices import PaymentMethod


class MobileMoneyForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+232 76 123 456',
            'inputmode': 'tel',
            'autocomplete': 'tel',
        }),
    )
    network = forms.ChoiceField(
        choices=[('orange', 'Orange Money'), ('afrimoney', 'AfriMoney'), ('qmoney', 'QMoney')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number'].strip()
        compact_number = ''.join(mobile_number.split())

        if compact_number.startswith('+232'):
            subscriber_number = compact_number[4:]
            if not subscriber_number.isascii() or not subscriber_number.isdigit() or len(subscriber_number) != 8:
                raise ValidationError('Enter a valid mobile number in international or local format.')
            return f'+232 {subscriber_number[:2]} {subscriber_number[2:5]} {subscriber_number[5:]}'

        if compact_number.startswith('+'):
            raise ValidationError('Enter a valid mobile number in international or local format.')

        if not compact_number.isascii() or not compact_number.isdigit() or len(compact_number) not in (8, 9):
            raise ValidationError('Enter a valid mobile number in international or local format.')

        if len(compact_number) == 9 and not compact_number.startswith('0'):
            raise ValidationError('Enter a valid mobile number in international or local format.')

        if len(compact_number) == 8 and compact_number.startswith('0'):
            raise ValidationError('Enter a valid mobile number in international or local format.')

        if len(compact_number) == 8:
            return f'{compact_number[:2]} {compact_number[2:5]} {compact_number[5:]}'
        return f'{compact_number[:3]} {compact_number[3:6]} {compact_number[6:]}'


class CardForm(forms.Form):
    card_holder = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}))
    expiry = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    cvv = forms.CharField(
        max_length=4,
        validators=[RegexValidator(r'^[0-9]{3,4}$', 'CVV must contain 3 or 4 digits.')],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'inputmode': 'numeric',
            'pattern': '[0-9]{3,4}',
            'autocomplete': 'cc-csc',
        }),
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        digits = card_number.replace(' ', '')
        if len(digits) != 16 or not digits.isascii() or not digits.isdigit():
            raise ValidationError('Card number must contain 16 digits.')
        return digits

    def clean_expiry(self):
        expiry = self.cleaned_data['expiry']
        if len(expiry) != 5 or expiry[2] != '/' or not expiry[:2].isascii() or not expiry[3:].isascii() or not expiry[:2].isdigit() or not expiry[3:].isdigit() or not 1 <= int(expiry[:2]) <= 12:
            raise ValidationError('Expiry date must be in MM/YY format.')

        return expiry
