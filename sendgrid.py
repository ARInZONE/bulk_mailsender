import sendgrid
import os
import pandas
from sendgrid.helpers.mail import Email, Content, Mail, Attachment
send = pandas.read_csv('em_sender_credentials_sendgrid.csv',names=['sender_email_ids','sendgrid_key_id','email_accounts_limit'])
for i in range(len(send)-1):
  count = int(send['email_accounts_limit'][1])
  # open the receiver's csv file for email ids and names
  rece = pandas.read_csv('em_recipient_email_ids.csv',names=['recipient_email_ids','recipient_first_name','recipient_middle_name','recipient_last_name'])
  for j in range(len(rece)-1):
    # open the csv file for body and subject of the mail
    body = pandas.read_csv('em_email_body.csv',names=['body_subject','body_filepath','body_cc','body_bcc','body_text'])
    sg = sendgrid.SendGridAPIClient(send['sendgrid_key_id'][1])
    from_email = Email(send['sender_email_ids'][1])
    to_email = Email(rece['em_recipient_email_ids'][1])
    subject = body['body_subject']
    content = Content("text/plain", body['body_text'])
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    send['email_accounts_limit'][1]=count
    send.to_csv('em_sender_credentials_sendgrid.csv', sep=',',index = False, header = False)