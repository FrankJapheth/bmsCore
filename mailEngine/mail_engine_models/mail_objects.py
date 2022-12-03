from django.db import models

from .mail_accounts import MailAccount
from .mail_boxes import MailBox
from .flags import Flag
from .label import Label


class MailObject(models.Model):
    mail_box = models.ForeignKey(to=MailBox, on_delete=models.CASCADE, null=True)
    mail_label = models.ForeignKey(to=Label, on_delete=models.CASCADE, null=True)
    mail_flag = models.ForeignKey(to=Flag, on_delete=models.CASCADE, null=True)
