from django.db import models
from django.utils import timezone
from .mail_objects import MailObject
from .mail_accounts import MailAccount


class MailHead(models.Model):
    sender = models.CharField(null=True, max_length=100)
    reply_to = models.CharField(null=True, max_length=100)
    recipient = models.CharField(null=True, max_length=100)
    recipient_email_address = models.CharField(null=True, max_length=100)
    subject = models.CharField(null=True, max_length=300)
    mail_date = models.DateTimeField(default=timezone.now)
    att_present = models.BooleanField(default=False)
    mail_server_id = models.IntegerField(null=True)
    mail_object = models.ForeignKey(to=MailObject, on_delete=models.CASCADE, null=True)
    mail_account = models.ForeignKey(to=MailAccount, on_delete=models.CASCADE, null=True)
