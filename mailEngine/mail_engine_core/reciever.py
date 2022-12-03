import email
from email.header import decode_header
import imaplib
import os


class MailReceiver:

    # Initializing the Receiving engine with mail engine credentials and user credentials

    def __init__(self,
                 mail_engine_address: str = "",
                 login_email_address: str = "",
                 login_password: str = "",
                 mail_engine_port: int = 0,
                 set_max_mails: int = 100,
                 set_last_mail: int = 0
                 ):

        self.mails_numb = None
        self.engine_address: str = mail_engine_address
        self.engine_port: str = mail_engine_port
        self.login_address: str = login_email_address
        self.login_password: str = login_password
        self.port_present: bool = False if self.engine_port == 0 else True
        self.max_mails: int = set_max_mails
        self.last_mail = set_last_mail

    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    def list_mail_account(self):

        if self.port_present:
            try:
                # create an IMAP4 object with SSL if port present
                imap = imaplib.IMAP4_SSL(self.engine_address, 993)
            except:
                print(
                    """There is a connection problem check if your Engine Address 
                    and engine port are correct and also check if your are connected 
                    to the internet then try again.""")
                exit()
            try:
                # authenticate
                imap.login(self.login_address, self.login_password)
            except:
                print("Log in failed check your credentials and try again.")
                exit()

            try:
                resp_code, directories = imap.list()
            except Exception as e:
                print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
                resp_code, directories = None, None

            for directory in directories:
                resp_code, mail_count = imap.select(mailbox=directory.decode().split('"."')[1], readonly=True)
                print("{} - {}".format(directory.decode().split('"."'), mail_count[0].decode()))

    def get_mail_heads(self, box_name: str, starting_point: int):

        fetched_heads = []
        if self.port_present:
            try:
                # create an IMAP4 object with SSL if port present
                imap = imaplib.IMAP4_SSL(self.engine_address, 993)
            except:
                print(
                    """There is a connection problem check if your Engine Address 
                    and engine port are correct and also check if your are connected 
                    to the internet then try again.""")
                exit()
            try:
                # authenticate
                imap.login(self.login_address, self.login_password)
            except:
                print("Log in failed check your credentials and try again.")
                exit()

            imap.select(mailbox=box_name, readonly=True)

            resp_code, mail_ids = imap.search(None, "ALL")

            for mail_id in mail_ids[0].decode().split()[starting_point:]:
                resp_code, mail_data = imap.fetch(mail_id, '(RFC822)')
                message = email.message_from_bytes(mail_data[0][1])
                attachment_present = False

                for part in message.walk():
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" in content_disposition:
                        attachment_present = True

                header_details_dict: dict = {
                    "From": self.decode_fetched_header(message.get("From")),
                    "To": self.decode_fetched_header(message.get("To")),
                    "Bcc": self.decode_fetched_header(message.get("Bcc")),
                    "Subject": self.decode_fetched_header(message.get("Subject")),
                    "Date": self.decode_fetched_header(message.get("Date")),
                    "MailId": mail_id,
                    "attachmentPresent": attachment_present

                }
                fetched_heads.append(header_details_dict)
            return fetched_heads

    def decode_fetched_header(self, fetched_header_to_decode):

        decoded_header_value = None

        try:

            decoded_header = decode_header(fetched_header_to_decode)
            if len(decoded_header) >= 1:
                decoded_header_details = decoded_header[0]
                if len(decoded_header_details) > 1:
                    if decoded_header_details[1] is not None:
                        decoded_header_content = decoded_header_details[0].decode(decoded_header_details[1])
                    else:
                        decoded_header_content = decoded_header_details[0]
                    if '<' in decoded_header_content and '>' in decoded_header_content:
                        decoded_header_content_value = decoded_header_content[
                                                       decoded_header_content.find(
                                                           '<') + 1: decoded_header_content.find('>')
                                                       ]
                        decoded_header_value = decoded_header_content_value
                    else:
                        decoded_header_value = decoded_header_content

        except TypeError:

            if fetched_header_to_decode is not None:
                if len(fetched_header_to_decode) >= 1:
                    header_detail_content = fetched_header_to_decode[0]

                    if len(header_detail_content) > 1:
                        header_detail_content_value = header_detail_content[0].decode(
                            header_detail_content[1])
                        decoded_header_value = header_detail_content_value

        return decoded_header_value

    def get_mail_body(self, mail_body_details: dict):
        msg_body_items = {"Attachments_present": False, "html_present": False}
        attachments_location = []
        try:
            # create an IMAP4 object with SSL if port present
            imap = imaplib.IMAP4_SSL(self.engine_address, 993)
        except:
            print(
                """There is a connection problem check if your Engine Address 
                    and engine port are correct and also check if your are connected 
                    to the internet then try again.""")
            exit()
        try:
            # authenticate
            imap.login(self.login_address, self.login_password)
        except:
            print("Log in failed check your credentials and try again.")
            exit()

        imap.select(mailbox=f'{mail_body_details["serverFlagName"]}', readonly=True)
        resp_code, mail_data = imap.fetch(f'{mail_body_details["mailServerId"]}', '(RFC822)')
        message = email.message_from_bytes(mail_data[0][1])

        if message.is_multipart():
            msg_body_items["type"] = "multipart"

            for part in message.walk():
                # extract content type and content_disposition of email part
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    # get the email body part content
                    body = part.get_payload(decode=True)
                except AttributeError:
                    body = None

                if content_type == "text/plain":
                    folder_name = f'media/{mail_body_details["mailObjId"]}/drafts'
                    if not os.path.isdir(folder_name):
                        # make a folder for text part of the email for it is editable
                        os.makedirs(folder_name)
                    file_name = "draft.txt"
                    file_path = os.path.join(folder_name, file_name)

                    with open(file_path, "wb") as txt_file:
                        txt_file.write(body)

                    txt_file_path = os.path.join(folder_name, file_name)
                    msg_body_items["text_file_location"] = txt_file_path

                elif content_type == "text/html":
                    msg_body_items["html_present"] = True
                    folder_name = f'media/{mail_body_details["mailObjId"]}/html'
                    if not os.path.isdir(folder_name):
                        # make a folder for this email
                        os.makedirs(folder_name)
                    file_name = "index.html"
                    file_path = os.path.join(folder_name, file_name)

                    # write the file
                    open(file_path, "wb").write(body)

                    html_file_path = os.path.join(folder_name, file_name)
                    msg_body_items["html_file_location"] = html_file_path

                if "attachment" in content_disposition:
                    attachment_main_type = part.get_content_maintype()
                    folder_name = f'media/{mail_body_details["mailObjId"]}/attachments'
                    if not os.path.isdir(folder_name):
                        # make a folder for this email
                        os.makedirs(folder_name)

                    filename = part.get_filename()
                    attachment_ext = os.path.splitext(filename)[1]
                    filepath = os.path.join(folder_name, filename)
                    with open(filepath, "wb") as attachment_file:
                        attachment_file.write(part.get_payload(decode=True))

                    attachment_details = {
                        'filename': filename,
                        'file_main_type': attachment_main_type,
                        'file_ext': attachment_ext,
                        'filePath': '/' + filepath
                    }

                    attachments_location.append(attachment_details)
                    msg_body_items["Attachments_present"] = True

                    msg_body_items["Attachments_folder"] = attachments_location

        else:

            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                try:
                    # get the email body part content
                    body = part.get_payload(decode=True)
                except AttributeError:
                    body = None

                if content_type == "text/plain":
                    msg_body_items["type"] = "singlepart"
                    folder_name = f'media/{mail_body_details["mailObjId"]}/drafts'

                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.makedirs(folder_name)

                    file_name = "draft.txt"
                    filepath = os.path.join(folder_name, file_name)
                    with open(filepath, "wb") as txt_file:
                        txt_file.write(body)
                    msg_body_items["text_file_location"] = filepath
                    msg_body_items["html_file_location"] = ''

                elif content_type == "text/html":
                    msg_body_items["html_present"] = True
                    folder_name = f'media/{mail_body_details["mailObjId"]}/html'
                    if not os.path.isdir(folder_name):
                        # make a folder for this email
                        os.makedirs(folder_name)
                    file_name = "index.html"
                    file_path = os.path.join(folder_name, file_name)

                    # write the file
                    open(file_path, "wb").write(body)

                    html_file_path = os.path.join(folder_name, file_name)
                    msg_body_items["html_file_location"] = html_file_path
                    msg_body_items["text_file_location"] = ''

        return msg_body_items
