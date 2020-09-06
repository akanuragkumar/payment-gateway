from rest_framework.views import APIView
from .services import PaymentService, PaymentDetailService

payment_method = PaymentService()
payment_detail = PaymentDetailService()


class PaymentMethodListCreateView(APIView):
    def post(self, request):
        """method for creating new payment method"""
        return payment_method.create(request=request)

    def get(self, request):
        """method for getting payment method list"""
        return payment_method.list(request=request)


class PaymentDetailListCreateView(APIView):
    def post(self, request):
        """method for creating new payment"""
        return payment_detail.create(request=request)
