from django.db import models
from .mail_accounts import MailAccount


class Contact(models.Model):
    account = models.ForeignKey(to=MailAccount, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.value
