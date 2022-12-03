# Generated by Django 4.1.3 on 2022-11-29 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailAccount',
            fields=[
                ('account_host_login_address', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('account_host_login_password', models.CharField(max_length=100, null=True)),
                ('account_host_engine_address', models.CharField(max_length=100)),
                ('account_name', models.CharField(max_length=100, null=True)),
                ('account_inbox', models.IntegerField(default=0, null=True)),
                ('account_outbox', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_name', models.CharField(max_length=100, null=True)),
                ('last_mail_id', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailbox')),
                ('mail_flag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.flag')),
                ('mail_label', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.label')),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailaccount')),
            ],
        ),
        migrations.CreateModel(
            name='MailHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100, null=True)),
                ('reply_to', models.CharField(max_length=100, null=True)),
                ('recipient', models.CharField(max_length=100, null=True)),
                ('recipient_email_address', models.CharField(max_length=100, null=True)),
                ('subject', models.CharField(max_length=300, null=True)),
                ('mail_date', models.DateTimeField(auto_now=True)),
                ('att_present', models.BooleanField(default=False)),
                ('mail_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailobject')),
            ],
        ),
        migrations.CreateModel(
            name='MailBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_url', models.CharField(max_length=300, null=True)),
                ('body_draft_url', models.CharField(max_length=300, null=True)),
                ('mail_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailobject')),
            ],
        ),
        migrations.CreateModel(
            name='MailAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.CharField(max_length=400, null=True)),
                ('mail_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailobject')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='label_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailaccount'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=150, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailEngine.mailaccount')),
            ],
        ),
    ]