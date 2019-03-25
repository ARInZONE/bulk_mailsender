import base64
import sendgrid
import os
import pandas
from sendgrid.helpers.mail import Email, Content, Mail, Attachment

send = pandas.read_csv('em_sender_credentials_sendgrid.csv',names=['sender_email_ids','sendgrid_key_id','email_accounts_limit'])
for i in range(len(send)-1):
  try:
      # Python 3
      import urllib.request as urllib
  except ImportError:
      # Python 2
      import urllib2 as urllib

  sg = sendgrid.SendGridAPIClient(send['sendgrid_key_id'][i+1])
  from_email = Email(send['sender_email_ids'][i+1])
  rece = pandas.read_csv('em_recipient_email_ids.csv',names=['recipient_email_ids','recipient_first_name','recipient_middle_name','recipient_last_name'])
  for j in range(len(rece)-1):
    body = pandas.read_csv('em_email_body.csv',names=['body_subject','body_filepath','body_cc','body_bcc','body_text'])
    subject = body['body_subject'][1]
    to_email = Email(rece['recipient_email_ids'][j+1])
    content = Content("text/html", body['body_text'][1])

    file_path = body['body_filepath'][1]
    with open(file_path,'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "application/txt"
    attachment.filename = file_path
    attachment.disposition = "attachment"
    attachment.content_id = "Example Content ID"

    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as e:
        print(e.read())
        exit()

    print(response.status_code)
    print(response.body)
    print(response.headers)