from django.db import models


class MailBox(models.Model):
    box_name = models.CharField(null=True, max_length=100)
    last_mail_id = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.box_name
