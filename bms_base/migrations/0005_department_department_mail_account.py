# Generated by Django 4.1.3 on 2022-12-02 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms_base', '0004_organization_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='department_mail_account',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
