import boto3
from botocore.exceptions import ClientError
import csv
import pandas
import os

# create the directory for aws credentials
dirName =os.environ['HOME']+'/.aws'
# open the sender csv file for sender email ids with respective key and id 
send = pandas.read_csv('em_sender_credentials_aws.csv',names=['sender_email_ids','aws_access_id','aws_key_id','email_accounts_limit'])
count = int(send['email_accounts_limit'][1])
# writes the key and id to /.aws/credentials file
if not os.path.exists(dirName):
    os.makedirs(dirName)
with open(dirName+"/credentials", "w") as key:
    key.write('[default]\naws_access_key_id = '+send['aws_access_id'][1]+'\naws_secret_access_key = '+send['aws_key_id'][1])
    key.close()
# open the receiver's csv file for email ids and names
rece = pandas.read_csv('em_recipient_email_ids.csv',names=['recipient_email_ids','recipient_first_name','recipient_middle_name','recipient_last_name'])
body = pandas.read_csv('em_email_body.csv',names=['body_subject','body_filepath','body_cc','body_bcc','body_text'])
# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"
# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)
# Try to send the email.
if(count<100):
    try:
        count+=1
        #Provide the contents of the email.
        response = client.send_raw_email(
        RawMessage={
            'Data': 'From: '+send['sender_email_ids'][1]+'\nTo: '
            +rece['recipient_email_ids'][1]+'\nSubject:'+body['body_subject'][1]
            +'\nMIME-Version: 1.0\nContent-type: Multipart/Mixed; boundary="NextPart"\n\n--NextPart\nContent-Type: text/plain\n\n'
            +body['body_text'][1]+'\n\n--NextPart\nContent-Type: text/plain;\nContent-Disposition: attachment; filename=\"'
            +body['body_filepath'][1]+'\"\n\nAttachment:\n\n--NextPart--',
        }
        #ConfigurationSetName='string'
    )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
else:
    print 'Error: limit crossed!'
send['email_accounts_limit'][1]=count
send.to_csv('em_sender_credentials_aws.csv', sep=',',index = False, header = False)

