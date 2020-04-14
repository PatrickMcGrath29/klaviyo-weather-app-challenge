import boto3
import requests
from botocore.exceptions import ClientError

SENDER = "Patrick McGrath <patrickmcgrath29@gmail.com>"
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"
SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

BODY_HTML = """
<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
"""


client = boto3.client('ses',region_name=AWS_REGION)

def lambda_handler(event, context):
    pass

def fetch_weather_data(location):
    res = requests.get('https://api.weatherbit.io/v2.0/forecast/daily', data = {
        'city': location,
        'country': 'US',
        'key': '9d9d424dad75474fa4a98d86de22d164',
        'days': 2
    })

    return res

def send_email(weather_data, recipient):
    try:
        client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )

    except ClientError as e:
        return False
    else:
        return True

