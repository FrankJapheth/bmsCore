from django.db import models

from .mail_objects import MailObject


class MailBody(models.Model):
    body_url = models.CharField(null=True, max_length=300)
    body_draft_url = models.CharField(null=True, max_length=300)
    mail_object = models.ForeignKey(
        to=MailObject,
        on_delete=models.CASCADE
    )
