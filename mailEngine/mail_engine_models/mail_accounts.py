from django.db import models


class MailAccount(models.Model):
    account_host_login_address = models.CharField(max_length=100, primary_key=True)
    account_host_login_password = models.CharField(max_length=100, null=True)
    account_host_engine_address = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100, null=True)
    account_inbox = models.IntegerField(default=0, null=True)
    account_outbox = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.account_name
