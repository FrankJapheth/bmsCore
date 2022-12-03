from django.db import models

from .flags import Flag
from .mail_accounts import MailAccount


class Label(models.Model):
    label_account = models.ForeignKey(to=MailAccount, on_delete=models.CASCADE, null=True)
    label_name = models.CharField(max_length=100, null=True)
    account_mails = models.IntegerField(default=0)
    label_flag = models.ForeignKey(to=Flag, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.label_name
