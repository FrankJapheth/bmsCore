from email.message import EmailMessage
import smtplib
import os


class MailSender:
    def __init__(self, engine_address, engine_port, user_name, password):
        self.engine_address = engine_address
        self.engine_port = engine_port
        self.user_name = user_name
        self.password = password

    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in str(text))

    def text_generator(self, mail_variables):
        text_paras = "<div>"

        for para in mail_variables["paras"]:
            text_para = f"<p>{para}</p>"
            text_paras += text_para

        text_paras += "</div>"

        html_text = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{mail_variables["organizationName"]}</title>
            </head>
            <body>
                <div class="holder">
                    <div class="mainbody">
                        {text_paras}
                    </div>
                </div>
            </body>
            </html>
        """

        return html_text

    def send_mail(self, mail_details):
        email_msg = EmailMessage()
        email_msg['from'] = self.user_name
        email_msg["replay_to"] = self.user_name
        email_msg['Subject'] = mail_details["subject"]
        email_msg["Cc"] = mail_details["cc"]
        email_msg["Bcc"] = mail_details["bcc"]
        email_msg['to'] = ''

        email_msg.set_content(mail_details["content"])
        email_msg.add_alternative(mail_details["body"], subtype='html')

        msg_body_items = {}

        folder_name = "media/" + self.clean(mail_details["objId"])

        if not os.path.isdir(folder_name + '/html'):
            # make a folder for this email (named after the subject)
            os.makedirs(folder_name + '/html')

        file_name = "index.html"
        file_path = os.path.join(folder_name + '/html/', file_name)

        with open(file_path, "wb") as txt_file:
            txt_file.write(mail_details["body"].encode("utf-8"))

        msg_body_items["text_file_location"] = file_path

        draft_file_name = "draft.txt"
        draft_file_path = os.path.join(folder_name + '/drafts/', draft_file_name)

        if not os.path.isdir(folder_name + '/drafts'):
            # make a folder for this email (named after the subject)
            os.makedirs(folder_name + '/drafts')

        with open(draft_file_path, "wb") as txt_file:
            txt_file.write(mail_details["body_draft"].encode("utf-8"))

        msg_body_items["draft_text_file_location"] = draft_file_path

        img_file_types = ['.JPG', '.PNG', '.GIF', '.WEBP', '.TIFF', '.PSD', '.RAW', '.BMP', '.HEIF', '.INDD', '.JPEG',
                          '.SVG', '.AI', '.EPS']
        video_fle_types = ['.WEBM', '.MPG', '.MP2', '.MPEG', '.MPE', '.MPV', '.OGG', '.MP4', '.M4P', '.M4V', '.AVI',
                           '.WMV', '.MOV', '.QT', '.FLV', '.SWF', '.AVCHD']
        msg_body_items["Attachments_present"] = False
        if len(mail_details["files_details"]) > 0:

            msg_body_items["Attachments_present"] = True

            for file_details in mail_details["files_details"]:
                file_type = os.path.splitext(file_details)[1]
                type_found = False
                attached_file_type = None

                file_name = file_details.split(os.sep)[len(file_details.split(os.sep)) - 1]

                for img_type in img_file_types:
                    if file_type.lower() == img_type.lower():
                        attached_file_type = "image"
                        type_found = True

                if not type_found:
                    for vid_type in video_fle_types:
                        if file_type.lower() == vid_type.lower():
                            attached_file_type = "Video"
                            type_found = True

                if type_found is False:
                    attached_file_type = "application"

                with open(file_details[1:], "rb") as attachment_file:
                    attachment_file_content = attachment_file.read()
                    email_msg.add_attachment(attachment_file_content, maintype=attached_file_type,
                                             subtype=file_type[1:], filename=file_name)

        msg_body_items["msg_sent"] = True
        for mail_receiver in mail_details["mailReceivers"]:

            with smtplib.SMTP_SSL(host=self.engine_address, port=self.engine_port) as smtp:
                smtp.login(self.user_name, self.password)
                try:
                    del email_msg['to']
                    email_msg['to'] = mail_receiver
                    smtp.send_message(email_msg)
                    smtp.close()

                except:
                    smtp.close()
                    msg_body_items["msg_sent"] = False

        return msg_body_items
