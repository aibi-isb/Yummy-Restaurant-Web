from django.test import SimpleTestCase

from .forms import CardForm, MobileMoneyForm


class MobileMoneyFormValidationTests(SimpleTestCase):
    def valid_data(self, mobile_number):
        return {
            'mobile_number': mobile_number,
            'network': 'orange',
            'amount': '10.00',
        }

    def test_accepts_international_number(self):
        form = MobileMoneyForm(self.valid_data('+232 76 123 456'))

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['mobile_number'], '+232 76 123 456')

    def test_accepts_local_numbers_with_or_without_leading_zero(self):
        for mobile_number, normalized_number in [
            ('76 123 456', '76 123 456'),
            ('076 123 456', '076 123 456'),
            ('+23276123456', '+232 76 123 456'),
        ]:
            with self.subTest(mobile_number=mobile_number):
                form = MobileMoneyForm(self.valid_data(mobile_number))

                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data['mobile_number'], normalized_number)

    def test_rejects_invalid_mobile_number_format(self):
        for mobile_number in ['+231 76 123 456', '76 123', '076 123 45', '76 123 456a']:
            with self.subTest(mobile_number=mobile_number):
                form = MobileMoneyForm(self.valid_data(mobile_number))

                self.assertIn('mobile_number', form.errors)
                self.assertEqual(
                    form.errors['mobile_number'][0],
                    'Enter a valid mobile number in international or local format.',
                )


class CardFormValidationTests(SimpleTestCase):
    def valid_data(self):
        return {
            'card_holder': 'Test User',
            'card_number': '4242 4242 4242 4242',
            'expiry': '12/30',
            'cvv': '123',
            'amount': '10.00',
        }

    def test_accepts_valid_card_data(self):
        form = CardForm(self.valid_data())

        self.assertTrue(form.is_valid())

    def test_rejects_invalid_card_number_format(self):
        data = self.valid_data()
        data['card_number'] = '4242-4242-4242-4242'

        form = CardForm(data)

        self.assertIn('card_number', form.errors)
        self.assertEqual(form.errors['card_number'][0], 'Card number must contain 16 digits.')

    def test_rejects_invalid_expiry_format(self):
        data = self.valid_data()
        data['expiry'] = '13/30'

        form = CardForm(data)

        self.assertIn('expiry', form.errors)
        self.assertEqual(form.errors['expiry'][0], 'Expiry date must be in MM/YY format.')

    def test_rejects_invalid_cvv_format(self):
        data = self.valid_data()
        data['cvv'] = '12a'

        form = CardForm(data)

        self.assertIn('cvv', form.errors)
        self.assertEqual(form.errors['cvv'][0], 'CVV must contain 3 or 4 digits.')
