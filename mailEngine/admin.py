from django.contrib import admin

from .mail_engine_models.mail_accounts import MailAccount
from .mail_engine_models.label import Label
from .mail_engine_models.flags import Flag
from .mail_engine_models.contacts import Contact
from .mail_engine_models.mail_objects import MailObject
from .mail_engine_models.mail_head import MailHead
from .mail_engine_models.mail_body import MailBody
from .mail_engine_models.mail_attachments import MailAttachment
from .mail_engine_models.mail_boxes import MailBox

admin.site.register(MailAccount)
admin.site.register(Label)
admin.site.register(Flag)
admin.site.register(Contact)
admin.site.register(MailObject)
admin.site.register(MailHead)
admin.site.register(MailBody)
admin.site.register(MailAttachment)
admin.site.register(MailBox)
