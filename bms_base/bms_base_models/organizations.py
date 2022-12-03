from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    organization_domain = models.CharField(null=False, max_length=150, primary_key=True)
    organization_name = models.CharField(null=False, max_length=150)
    organization_mail_server = models.CharField(null=False, max_length=150)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    organization_date_created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.organization_name

