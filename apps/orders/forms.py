from django import forms


class CheckoutForm(forms.Form):
    street = forms.CharField(
        label='Street Address',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Main St'}),
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Freetown'}),
    )
    state = forms.CharField(
        label='Region or Province',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Western Area'}),
    )
    zip_code = forms.CharField(
        label='ZIP Code',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1000'}),
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+232 76 767 676'}),
    )
    delivery_time = forms.ChoiceField(
        choices=[
            ('asap', 'As soon as possible'),
            ('30min', 'In 30 minutes'),
            ('1hr', 'In 1 hour'),
            ('scheduled', 'Schedule for later'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    delivery_notes = forms.CharField(
        required=False,
        label='Special Instructions (optional)',
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Any special instructions for your order...'}),
    )

    def delivery_address(self):
        data = self.cleaned_data
        notes = data.get('delivery_notes', '').strip()
        address = (
            f"{data['street']}, {data['city']}, {data['state']} {data['zip_code']}\n"
            f"Phone: {data['phone']}\n"
            f"Delivery: {dict(self.fields['delivery_time'].choices)[data['delivery_time']]}"
        )
        if notes:
            address += f"\nNotes: {notes}"
        return address
