# Generated by Django 4.1.3 on 2022-12-03 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailEngine', '0011_label_account_mails_label_label_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='account_mails',
            field=models.IntegerField(default=0),
        ),
    ]