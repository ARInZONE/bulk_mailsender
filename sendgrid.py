import sendgrid
import os
import pandas

send = pandas.read_csv('em_sender_credentials_sendgrid.csv',names=['sender_email_ids','sendgrid_key_id','email_accounts_limit'])
count = int(send['email_accounts_limit'][1])
# open the receiver's csv file for email ids and names
rece = pandas.read_csv('em_recipient_email_ids.csv',names=['recipient_email_ids','recipient_first_name','recipient_middle_name','recipient_last_name'])
# open the csv file for body and subject of the mail
body = pandas.read_csv('em_email_body.csv',names=['body_subject','body_filepath','body_cc','body_bcc','body_text'])
sg = sendgrid.SendGridAPIClient(apikey=send['sendgrid_key_id'][1])
print send['sendgrid_key_id'][1]
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": rece['em_recipient_email_ids']
        }
      ],
      "subject": rece['body_subject']
    }
  ],
  "from": {
    "email": send['sender_email_ids'][1]
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Arya stark will die."
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)
send['email_accounts_limit'][1]=count
send.to_csv('em_sender_credentials_sendgrid.csv', sep=',',index = False, header = False)