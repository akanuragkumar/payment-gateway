from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from jsonschema import validate
from datetime import datetime
import math
from payment_api.models import PaymentMethod, PaymentDetail
from payment_api.serializers import PaymentMethodSerializer, PaymentDetailSerializer


class PaymentService:
    def create(self, request):
        """ Create new payment method"""
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'type': serializer.data['type'],
                'subtype': serializer.data['subtype']
            })
        # returning validation errors
        return Response({
            'error': serializer.errors
        })

    def list(self, request):
        queryset = PaymentMethod.objects.filter(is_active=True)
        serializer = PaymentMethodSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class PaymentDetailService:
    def validate_payment_data(self, request):
        payment_data_schema = {
            "type": "object",
            "properties": {
                    "number": {"type": "number"},
                    "expirationMonth": {"type": "number"},
                    "expirationYear": {"type": "number"},
                    "cvv": {"type": "number"},
            },
            "required": ["number", "expirationMonth", "expirationYear", "cvv"]
        }
        return validate(instance=request.data['card'], schema=payment_data_schema)

    def create(self, request):
        """ Making new payment """
        try:
            PaymentDetailService.validate_payment_data(self, request)
        except:
            return Response({
                'error': 'Card detail data is not correct'
            }, status=status.HTTP_400_BAD_REQUEST)
        """check the card number count, it should be always equal to 16, else throw appropriate error"""
        card_number_count = int(math.log10(request.data['card']['number']))+1
        if card_number_count == 16:
            pass
        else:
            return Response({
                    'error': 'your card number is not of 16 digits'
                }, status=status.HTTP_400_BAD_REQUEST)
        """chech the card expiry, if expired return appropriate response"""
        today = datetime.today()
        month_year = str(datetime(today.year, today.month, 1))[:-9].split('-')
        current_year = int(month_year[0])
        current_month = int(month_year[1])
        expirationMonth = str(request.data['card']['expirationMonth'])
        expirationYear = int(request.data['card']['expirationYear'])
        if expirationMonth[0] == "0":
            expirationMonth = int(expirationMonth[1:2])
        expirationMonth = int(expirationMonth)
        if expirationYear > current_year:
            pass
        elif expirationYear == current_year:
            if expirationMonth >= current_month:
                pass
            else:
                return Response({
                    'error': 'your card is expired'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'your card is expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            payment_method_data = PaymentMethod.objects.filter(subtype=request.data['type'], is_active=True)
            currency_data = PaymentMethod.objects.filter(subtype=request.data['currency'], is_active=True)
            if payment_method_data[0] and currency_data[0]:
                pass
        except:
            return Response({
                'error': 'Payment method or currency not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentDetailSerializer(data=request.data)
        if serializer.is_valid():
            data_object = serializer.save()
            return Response({
                'type': serializer.data['type'],
                'currency': serializer.data['currency'],
                'amount': serializer.data['amount'],
                'card': {'number': serializer.data['card']['number']},
                'status': data_object.status,
                'authorization_code': data_object.payment_uuid,
                'time': str(data_object.created_on).replace("T", " ").replace(".000Z", "")[:-13]
            })
        # returning validation errors
        return Response({
            'error': serializer.errors
        })
