from django.db import models
from .mail_objects import MailObject


class MailAttachment(models.Model):
    file_url = models.CharField(null=True, max_length=400)
    file_name = models.CharField(null=True, max_length=150)
    file_type = models.CharField(null=True, max_length=150)
    file_extension = models.CharField(null=True, max_length=150)
    mail_object = models.ForeignKey(to=MailObject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.file_name
