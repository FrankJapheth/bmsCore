# Generated by Django 4.1.3 on 2022-12-04 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailEngine', '0012_alter_label_account_mails'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailobject',
            name='user_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailaccount'),
        ),
    ]
