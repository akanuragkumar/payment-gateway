import json
from rest_framework.test import APITestCase
from django.urls import reverse
from payment_api.models import PaymentMethod, PaymentDetail


class PaymentMethodAPIViewTestCase(APITestCase):
    url = reverse('payment-method-list')

    def test_create_payment_method(self):
        response = self.client.post(self.url, {
            "type": "currency",
            "subtype": "Euro"
        })
        self.assertEqual(200, response.status_code)

    def test_create_payment_method_2(self):
        response = self.client.post(self.url, {
            "type": "payment_type",
            "subtype": "Debit Card"
        })
        self.assertEqual(200, response.status_code)

    def test_payment_method_object(self):
        """
        Test to verify payment method get list
        """
        PaymentMethod.objects.create(
            type='currency', subtype='Euro')
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == PaymentMethod.objects.count())


class TodoListCreateAPIViewTestCase(APITestCase):
    url_payment_detail = reverse('payment-detail-list')
    url_payment_method = reverse('payment-method-list')

    def test_create_payment_detail(self):
        response_payment_method_currency = self.client.post(self.url_payment_method, {
            "type": "currency",
            "subtype": "Euro"
        })
        self.assertEqual(200, response_payment_method_currency.status_code)

        response_payment_method_type = self.client.post(self.url_payment_method, {
            "type": "payment_type",
            "subtype": "Debit Card"
        })
        self.assertEqual(200, response_payment_method_type.status_code)

        response_payment_detail = self.client.post(self.url_payment_detail,
                                                   {"currency": "Euro", "type": "Debit Card", "amount": 500,
                                                    "card": {"number": 4111111111111111, "expirationMonth": 2,
                                                             "expirationYear": 2020, "cvv": 111}},
                                                   format='json')
        self.assertEqual(200, response_payment_detail.status_code)

    def test_create_payment_detail_invalid_card_type(self):
        response_payment_method_currency = self.client.post(self.url_payment_method, {
            "type": "currency",
            "subtype": "Euro"
        })
        self.assertEqual(200, response_payment_method_currency.status_code)

        response_payment_method_type = self.client.post(self.url_payment_method, {
            "type": "payment_type",
            "subtype": "Debit Card"
        })
        self.assertEqual(200, response_payment_method_type.status_code)

        response_payment_detail = self.client.post(self.url_payment_detail,
                                                   {"currency": "Euro", "type": "Master Card", "amount": 500,
                                                    "card": {"number": 4111111111111111, "expirationMonth": 2,
                                                             "expirationYear": 2020, "cvv": 111}},
                                                   format='json')
        self.assertEqual(404, response_payment_detail.status_code)

    def test_create_payment_detail_invalid_card_data(self):
        response_payment_method_currency = self.client.post(self.url_payment_method, {
            "type": "currency",
            "subtype": "Euro"
        })
        self.assertEqual(200, response_payment_method_currency.status_code)

        response_payment_method_type = self.client.post(self.url_payment_method, {
            "type": "payment_type",
            "subtype": "Debit Card"
        })
        self.assertEqual(200, response_payment_method_type.status_code)

        response_payment_detail = self.client.post(self.url_payment_detail,
                                                   {"currency": "Euro", "type": "Debit Card", "amount": 500,
                                                    "card": {"number": 4111111111111111, "expirationMonth": 2,
                                                             "expirationYear": 2020}},
                                                   format='json')
        self.assertEqual(400, response_payment_detail.status_code)
