import datetime
import json
import os.path

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view

from django.core.files.storage import FileSystemStorage

from .models import MailObjectModel
from .models import MailObject
from .models import MailBox
from .models import Flag
from .models import MailAccount
from .models import MailFlagsModel
from .models import MailAttachment
from .models import MailAttachmentModel
from .models import MailHeadModel
from .models import MailHead
from .models import MailBodyModel
from .models import MailBody
from .models import Label

from .mail_engine_core.sender import MailSender
from .mail_engine_core.reciever import MailReceiver

smtp_engine_port = 465
imap_engine_port = 995


def json_resp(resp_data):
    bms_base_json_response = {'backendResponse': resp_data}
    resp = JsonResponse(bms_base_json_response, safe=False)
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Author"] = "adedefranklyne@gmail.com"
    return resp


def save_file(file_path, file_data):
    fs = FileSystemStorage()
    name = fs.save(file_path.replace(" ", ""), file_data)
    file_url = fs.url(name)
    return file_url


def write_to_file(dir_path, file_name, file_data) -> bool:
    file_path = dir_path + file_name
    wrote_successful = True
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    with open(file_path, "wb+") as f:
        f.write(file_data.encode('UTF-8'))

    return wrote_successful


@api_view(['POST'])
def create_mail_object(request):
    mail_object_details = request.data
    mail_object_model = MailObjectModel()
    mail_head_model = MailHeadModel()

    account_host_login_address = MailAccount.objects.get(
        account_host_login_address=mail_object_details['objectMailAccount'])
    mail_flag = Flag.objects.get(id=mail_object_details['mailFlagId'])

    mail_object_details = {
        'mailFlag': mail_flag,
        'userAccount': account_host_login_address,
        'objectMailAccount': mail_object_details['objectMailAccount'],
        'mailFlagId': mail_object_details['mailFlagId']

    }

    created_mail_object: MailObject = mail_object_model.create_mail_object(mail_object_details)
    created_mail_head: MailHead = mail_head_model.create_mail_head(mail_object_details, created_mail_object)

    draft_file_url = f'media/{created_mail_object.id}/drafts/'
    draft_init_content = 'Dhana LTD'

    write_to_file(draft_file_url, 'draft.txt', draft_init_content)
    mail_object_details['draftBodyUrl'] = draft_file_url
    mail_object_details['bodyUrl'] = ''

    mail_body_model = MailBodyModel()

    created_mail_body: MailBody = mail_body_model.create_mail_body(mail_object_details, created_mail_object)

    mail_object_response: dict = {
        'mail_object_id': created_mail_object.id,
        'sender': created_mail_head.sender,
        'reply_to': created_mail_head.reply_to,
        'mailBodyId': created_mail_body.id
    }

    return json_resp(mail_object_response)


@api_view(['POST'])
def get_system_flags(request):
    mails_flags = MailFlagsModel()

    label_account_id = request.data['accountId']

    account_host_login_address = MailAccount.objects.get(
        account_host_login_address=label_account_id)

    mail_flags_to_send = []

    mail_flags = mails_flags.get_mail_flags()

    for mail_flag in mail_flags:
        try:
            Label.objects.get(
                label_account__account_host_login_address=account_host_login_address.account_host_login_address,
                label_flag__id=mail_flag.id
            )
        except Label.DoesNotExist:
            new_label = Label()
            new_label.label_account = account_host_login_address
            new_label.label_flag = mail_flag
            new_label.label_name = account_host_login_address.account_name + "_" + mail_flag.name
            new_label.save()

        mail_flag_to_send = {
            'flagId': mail_flag.id,
            'flagName': mail_flag.name,
            'flagImapName': mail_flag.flag_imap_label
        }

        mail_flags_to_send.append(mail_flag_to_send)

    return json_resp(mail_flags_to_send)


@api_view(['POST'])
def get_mail_heads(request):
    flag_id = request.data['flagId']
    system_flag: Flag = Flag.objects.get(id=flag_id)
    system_account_user = MailAccount.objects.get(
        account_host_login_address=request.data['objectMailAccount'])

    mail_receiver: MailReceiver = MailReceiver(
        mail_engine_address=system_account_user.account_host_engine_address,
        mail_engine_port=imap_engine_port,
        login_email_address=system_account_user.account_host_login_address,
        login_password=system_account_user.account_host_login_password
    )
    if system_flag.flag_imap_label is not None:
        flag_label = Label.objects.get(
            label_account__account_host_login_address=request.data['objectMailAccount'],
            label_flag__id=flag_id
        )
        try:
            fetched_heads = mail_receiver.get_mail_heads(system_flag.flag_imap_label, int(flag_label.account_mails))
            if len(fetched_heads) > 0:
                flag_label.account_mails = fetched_heads[len(fetched_heads) - 1]['MailId']
                flag_label.save()

            for fetched_head in fetched_heads:

                try:
                    mail_date = datetime.datetime.strptime(fetched_head['Date'], '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    try:
                        mail_date = datetime.datetime.strptime(fetched_head['Date'], '%a, %d %b %Y %H:%M:%S %Z')
                    except:
                        mail_date = timezone.now()
                except TypeError:
                    mail_date = timezone.now()

                fetched_head_mail_object = MailObject()
                fetched_head_mail_object.mail_box = system_flag.mail_box
                fetched_head_mail_object.mail_flag = system_flag
                fetched_head_mail_object.save()
                fetched_mail_head: MailHead = MailHead()
                fetched_mail_head.sender = fetched_head['From']
                fetched_mail_head.reply_to = fetched_head['From']
                fetched_mail_head.recipient = fetched_head['To']
                fetched_mail_head.recipient_email_address = fetched_head['To']
                fetched_mail_head.subject = fetched_head['Subject']
                fetched_mail_head.mail_date = mail_date
                fetched_mail_head.att_present = fetched_head['attachmentPresent']
                fetched_mail_head.mail_server_id = fetched_head['MailId']
                fetched_mail_head.mail_object = fetched_head_mail_object
                fetched_mail_head.mail_account = system_account_user
                fetched_mail_head.save()
        except SystemExit:
            fetched_heads = []

    system_mail_heads = MailHead.objects.filter(
        mail_object__mail_flag__id=system_flag.id,
        mail_account__account_host_login_address=request.data['objectMailAccount'],
    ).order_by('-mail_date')
    mail_heads_to_send = []

    for system_mail_head in system_mail_heads:
        mail_head_to_send = {
            'mailObjectId': system_mail_head.mail_object.id,
            'mailSubject': system_mail_head.subject,
            'sender': system_mail_head.sender,
            'mailServerId': system_mail_head.mail_server_id,
            'date': system_mail_head.mail_date,
            'mailHeadId': system_mail_head.id
        }
        mail_heads_to_send.append(mail_head_to_send)

    return json_resp(mail_heads_to_send)


@api_view(['POST'])
def add_attachment(request):
    attachment_details = request.data

    attachment_file = attachment_details['attFile']
    attachment_file_name = attachment_details['fileName']
    attachment_file_type = attachment_details['fileType']
    file_extension = os.path.splitext(attachment_file_name)[1]
    object_id = attachment_details['objectId']

    attachment_file_path = f"{object_id}/attachments/{attachment_file_name}"

    attachment_file_url = save_file(attachment_file_path, attachment_file)

    mail_object = MailObject.objects.get(id=object_id)

    attachment_db_details = {
        'fileUrl': attachment_file_url,
        'fileName': attachment_file_name,
        'fileType': attachment_file_type,
        'fileExt': file_extension,
        'mailObject': mail_object,
    }

    mail_att_md = MailAttachmentModel()
    created_att = mail_att_md.create_ttachment(attachment_db_details)
    add_attachment_resp = {
        'attId': created_att.id,
        'attExt': created_att.file_extension,
        'attLink': created_att.file_url
    }

    return json_resp(add_attachment_resp)


@api_view(['POST'])
def send_mail(request):
    mail_details: dict = request.data

    sender_account: MailAccount = MailAccount.objects.get(account_host_login_address=mail_details['memberId'])

    mail_sender: MailSender = MailSender(
        engine_address=sender_account.account_host_engine_address,
        engine_port=smtp_engine_port,
        user_name=sender_account.account_host_login_address,
        password=sender_account.account_host_login_password
    )

    mail_text_content = ''

    for text_content in json.loads(mail_details['paras']):
        mail_text_content += '\n' + text_content

    html_text_generator_details = {

        'organizationName': mail_details['organizationName'],
        'paras': json.loads(mail_details['paras'])
    }

    mail_html_content = mail_sender.text_generator(html_text_generator_details)

    mail_to_send_details = {
        'content': mail_text_content,
        'body': mail_html_content,
        'body_draft': mail_text_content,
        'files_details': json.loads(mail_details['attachments']),
        'mailReceivers': json.loads(mail_details['receivers']),
        'subject': mail_details['subject'],
        'cc': json.loads(mail_details['cc']),
        'bcc': json.loads(mail_details['bcc']),
        'objId': mail_details['objId'],

    }

    mail_sent_details = mail_sender.send_mail(mail_to_send_details)

    mail_object = MailObject.objects.get(id=mail_details['objId'])

    if mail_sent_details['msg_sent'] is True:
        mail_flag_sent = Flag.objects.get(name='Sent')
        mail_object.mail_flag = mail_flag_sent

    mail_head: MailHead = MailHead.objects.get(mail_object__id=mail_object.id)
    mail_head.recipient = mail_details['receivers'][0]
    mail_head.recipient_email_address = mail_details['receivers'][0]
    mail_head.subject = mail_details['subject']
    mail_head.mail_account = sender_account

    mail_head.att_present = mail_sent_details['Attachments_present']

    mail_body: MailBody = MailBody.objects.get(mail_object__id=mail_object.id)

    mail_body.body_url = mail_sent_details['text_file_location']
    mail_body.body_draft_url = mail_sent_details['draft_text_file_location']

    mail_object.save()
    mail_head.save()
    mail_body.save()

    msg_sent_resp = {
        'msgSent': mail_sent_details['msg_sent']
    }

    return json_resp(msg_sent_resp)


@api_view(['POST'])
def get_mail_body(request):
    flag_id = request.data['flagId']
    mail_server_id = request.data['mailServerId']
    system_flag: Flag = Flag.objects.get(id=flag_id)
    system_mail_object = MailObject.objects.get(id=request.data['mailObjectId'])
    system_account_user = MailAccount.objects.get(
        account_host_login_address=request.data['objectMailAccount'])

    requested_body = MailBody.objects.filter(mail_object__id=request.data['mailObjectId'])

    if len(requested_body) <= 0:

        mail_receiver: MailReceiver = MailReceiver(
            mail_engine_address=system_account_user.account_host_engine_address,
            mail_engine_port=imap_engine_port,
            login_email_address=system_account_user.account_host_login_address,
            login_password=system_account_user.account_host_login_password
        )

        fetch_mail_details = {
            'mailServerId': mail_server_id,
            'serverFlagName': system_flag.flag_imap_label,
            'mailObjId': system_mail_object.id,
        }

        mail_body_details = mail_receiver.get_mail_body(fetch_mail_details)

        mail_body = MailBody()
        mail_body.body_draft_url = mail_body_details['text_file_location']
        mail_body.mail_object = system_mail_object

        if mail_body_details['html_present'] is True:
            mail_body.body_url = mail_body_details['html_file_location']
        if mail_body_details['Attachments_present'] is True:
            for attachment_details in mail_body_details['Attachments_folder']:
                mail_attachment = MailAttachment()
                mail_attachment.mail_object = system_mail_object
                mail_attachment.file_url = attachment_details['filePath']
                mail_attachment.file_name = attachment_details['filename']
                mail_attachment.file_type = attachment_details['file_main_type']
                mail_attachment.file_extension = attachment_details['file_ext']
                mail_attachment.save()
        mail_body.save()

    get_mail_body_resp = {
        'bodyType': '',
        'mail_body': '',
        'attachments': '',
        'mailBodyId': ''
    }

    gotten_body = MailBody.objects.get(mail_object__id=request.data['mailObjectId'])
    get_mail_body_resp['mailBodyId'] = gotten_body.id
    mail_body_atts = MailAttachment.objects.filter(mail_object__id=request.data['mailObjectId'])
    mail_body_atts_to_send = []
    for mail_body_att in mail_body_atts:
        mail_body_att_to_send = {
            'filename': mail_body_att.file_name,
            'fileType': mail_body_att.file_type,
            'fileUrl': mail_body_att.file_url,
            'fileExt': mail_body_att.file_extension,
            'fileId': mail_body_att.id
        }
        mail_body_atts_to_send.append(mail_body_att_to_send)

    get_mail_body_resp['attachments'] = mail_body_atts_to_send

    if gotten_body.body_url is not None:
        with open(gotten_body.body_url, "r", encoding="utf-8") as htmlFile:
            file_data = htmlFile.read()
            get_mail_body_resp['mail_body'] = file_data
            get_mail_body_resp['bodyType'] = 'HTML'
    elif gotten_body.body_draft_url is not None:
        with open(gotten_body.body_draft_url, "r", encoding="utf-8") as textFile:
            file_data = textFile.read()
            get_mail_body_resp['mail_body'] = file_data
            get_mail_body_resp['bodyType'] = 'TEXT'

    read_flag = Flag.objects.get(name='Read')
    mail_body_object = MailObject.objects.get(id=request.data['mailObjectId'])
    if mail_body_object.mail_flag.name == 'Unread':
        mail_body_object.mail_flag = read_flag
        mail_body_object.save()
        print('Done')
    return json_resp(get_mail_body_resp)


@api_view(['POST'])
def change_mail_flag(request):
    mail_flag_to_change_to_id = request.data['mailFlagId']
    mail_object_id_to_change = request.data['MailObjId']

    system_flag = Flag.objects.get(id=mail_flag_to_change_to_id)

    mail_obj_to_change = MailObject.objects.get(id=mail_object_id_to_change)

    mail_obj_to_change.mail_flag = system_flag
    mail_obj_to_change.save()

    return json_resp(True)


@api_view(['POST'])
def clear_mail_flag(request):
    mail_flag_to_change_to_id = request.data['mailFlagId']

    mail_objects = MailObject.objects.filter(mail_flag__id=mail_flag_to_change_to_id)

    for mail_object in mail_objects:
        mail_object.delete()

    return json_resp(True)
