from django.db import models
from django.contrib.auth.models import User

from .departments import Department


class Member(models.Model):
    member_id = models.CharField(null=False, max_length=150, primary_key=True)

    member_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    member_department = models.ForeignKey(to=Department, on_delete=models.CASCADE)

    member_date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.member_user.first_name + " " + self.member_user.last_name

