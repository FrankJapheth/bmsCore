from django.db import models
from .mail_boxes import MailBox


class Flag(models.Model):
    name = models.CharField(max_length=100, null=True)
    flag_prominence = models.IntegerField(null=True)
    flag_imap_label = models.CharField(max_length=100, null=True)
    mail_number = models.IntegerField(default=0)
    mail_box = models.ForeignKey(to=MailBox, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
