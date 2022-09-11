'''
This program interact with AWS cloud where it create a client with some permissions
With S3 uploads some files with contacts to be subscribed with the SNS tool.
'''

import boto3
import pandas as pd

aws_id = '__'
aws_key = '__'

#Creating the user
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id = aws_id,
    aws_secret_access_key = aws_key
    )

#Creating a bucket
bucket = s3.create_bucket(Bucket='my-gid-requests')

#Uploading a file to the cloud with AWS S3
s3.upload_file(
    Filename='contacts.csv',
    Bucket='my-gid-requests',
    Key='contacts.csv',
    ExtraArgs={'ACL':'public-read'}
    )

s3.upload_file(
    Filename='final_report.csv',
    Bucket='my-gid-requests',
    Key='final_report.csv',
    ExtraArgs={'ACL':'public-read'}
    )

#Creating a notification system with AWS SNS
sns = boto3.client(
    'sns',
    region_name='us-east-1',
    aws_access_key_id=aws_id,
    aws_secret_access_key = aws_key
    )

trash_arn = sns.create_topic(Name = "trash_notifications")['TopicArn']
streets_arn = sns.create_topic(Name = "streets_notifications")['TopicArn']

contacts = pd.read_csv('https://my-gid-requests.s3.amazonaws.com/contacts.csv')

#Subscribing users to topics
def subscribe_user(user_row):
    if user_row['Department'] == 'trash':
        sns.subscribe(TopicArn = trash_arn, Protocol='sms', Endpoint= str(user_row['Phone']))
        sns.subscribe(TopicArn = trash_arn, Protocol='email', Endpoint=user_row['Email'])
    else:
        sns.subscribe(TopicArn = streets_arn, Protocol='sms', Endpoint= str(user_row['Phone']))
        sns.subscribe(TopicArn = streets_arn, Protocol='email', Endpoint=user_row['Email'])

contacts.apply(subscribe_user, axis=1)

df = pd.read_csv('https://my-gid-requests.s3.amazonaws.com/final_report.csv')
df.set_index('service_name', inplace=True)

trash_violations_count = df.at['Illegal Dumping', 'count']
streets_violations_count = df.at['Pothole', 'count']

#Some statements to send SMS and email messages
if trash_violations_count > 100:
    message = "Trash violations cout is now {}".format(trash_violations_count)
    sns.publish(
        TopicArn = trash_arn,
        Message = message,
        Subject = "Trash Alert"
        )

if streets_violations_count > 30:
    message = "Streets violations cout is now {}".format(streets_violations_count)
    sns.publish(
        TopicArn = streets_arn,
        Message = message,
        Subject = "Streets Alert"
        )


