from django.db import models

from .organizations import Organization


class Department(models.Model):
    department_id = models.CharField(max_length=150, null=False, primary_key=True)
    department_name = models.CharField(max_length=150, null=False)
    department_organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    department_mail_account = models.CharField(max_length=150, null=True)

    department_date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name
