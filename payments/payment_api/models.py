import uuid as uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
import jsonfield


class BaseModel(models.Model):
    """parent model which will be inherited by all other child models"""
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class PaymentMethod(BaseModel):
    type = models.CharField(max_length=100, default='', editable=False)
    subtype = models.CharField(primary_key=True, max_length=100, default='', editable=False, db_index=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'It tells if fields can be active or not. '
            'Unselect this instead of deleting.'
        ),
    )
    modified_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'payment_methods'
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')

 
class PaymentDetail(BaseModel):
    type = models.CharField(max_length=100, null=False)
    currency = models.CharField(max_length=100, null=False)
    amount = models.FloatField(null=False)
    card = jsonfield.JSONField()
    status = models.CharField(max_length=100)
    payment_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        db_table = 'payment_details'
        verbose_name = _('Payment Detail')
        verbose_name_plural = _('Payment Details')

    def __str__(self):
        return self.payment_uuid.__str__()
