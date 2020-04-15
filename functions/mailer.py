import boto3
import urllib3
import json
from botocore.exceptions import ClientError

client = boto3.client('ses',region_name='us-east-1')

BODY_HTML = """
<html>
<head></head>
<body>
  <h1>{}</h1>
  <p>It's currently {} celsius in {}</p>
</body>
</html>
"""


def lambda_handler(event, context):
    entry = json.loads(event['Records'][0]['body'])
    weather_data = fetch_weather_data(entry['location'])

    tag_line = "Enjoy a discount on us."

    todays_description = weather_data[0]['weather']['description']
    todays_temp = weather_data[0]['temp']
    todays_precipitation = weather_data[0]['precip']
    tomorrows_temp = weather_data[1]['temp']

    if todays_description == 'Sunny' or todays_temp >= tomorrows_temp - 5:
        tag_line = "Its nice out! Enjoy a discount on us."
    elif todays_precipitation > 0 or todays_temp - 5 <= tomorrows_temp:
        tag_line = "Not so nice out? That's okay, enjoy a discount on us."

    return send_email(entry['email_address'], entry['location'], tag_line, todays_temp)

def fetch_weather_data(location):
    http = urllib3.PoolManager()
    res = http.request('GET', 'https://api.weatherbit.io/v2.0/forecast/daily?city={}&country=us&days=2&key={}'.format(
        location,
        '9d9d424dad75474fa4a98d86de22d164'
    ))

    return json.loads(res.data)['data']

def send_email(recipient, location, tag_line, temperature):
    email_body = BODY_HTML.format(tag_line, temperature, location)
    sender = "Patrick McGrath <hello@patrickmcgrath.io>"
    charset = "UTF-8"

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
                        'Charset': charset,
                        'Data': email_body,
                    }
                },
                'Subject': {
                    'Charset': charset,
                    'Data': tag_line,
                },
            },
            Source=sender
        )

    except ClientError as e:
        print(e)
        return False
    else:
        return True

