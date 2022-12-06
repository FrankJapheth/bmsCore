
from django.utils import timezone

from .mail_engine_models.mail_accounts import MailAccount
from .mail_engine_models.label import Label
from .mail_engine_models.flags import Flag
from .mail_engine_models.contacts import Contact
from .mail_engine_models.mail_objects import MailObject
from .mail_engine_models.mail_head import MailHead
from .mail_engine_models.mail_body import MailBody
from .mail_engine_models.mail_attachments import MailAttachment
from .mail_engine_models.mail_boxes import MailBox


class MailObjectModel:

    def create_mail_object(self, mail_object_details: dict) -> MailObject:
        created_mail_object: MailObject = MailObject()
        created_mail_object.mail_box = MailBox.objects.get(box_name='Outbox')
        created_mail_object.mail_flag = mail_object_details['mailFlag']
        created_mail_object.user_account = mail_object_details['userAccount']
        created_mail_object.save()

        return created_mail_object


class MailFlagsModel:

    def get_mail_flags(self):
        gotten_flags = Flag.objects.all().order_by('flag_prominence')
        return gotten_flags


class MailAttachmentModel:

    def create_ttachment(self, attachment_details: dict) -> MailAttachment:
        created_attachment = MailAttachment()

        created_attachment.file_url = attachment_details['fileUrl']
        created_attachment.file_name = attachment_details['fileName']
        created_attachment.file_type = attachment_details['fileType']
        created_attachment.file_extension = attachment_details['fileExt']
        created_attachment.mail_object = attachment_details['mailObject']
        created_attachment.save()

        return created_attachment


class MailHeadModel:

    def create_mail_head(self, mail_head_details: dict, mail_object: MailObject, mail_account: MailAccount) -> MailHead:
        created_mail_head: MailHead = MailHead()

        created_mail_head.sender = mail_head_details['objectMailAccount']
        created_mail_head.reply_to = mail_head_details['objectMailAccount']
        created_mail_head.mail_date = timezone.now()
        created_mail_head.mail_object = mail_object
        created_mail_head.mail_account = mail_account
        created_mail_head.save()

        return created_mail_head


class MailBodyModel:

    def create_mail_body(self, mail_body_details: dict, mail_body_object: MailObject) -> MailBody:
        created_mail_body = MailBody()
        created_mail_body.body_url = mail_body_details['bodyUrl']
        created_mail_body.body_draft_url = mail_body_details['draftBodyUrl']
        created_mail_body.mail_object = mail_body_object
        created_mail_body.save()

        return created_mail_body
