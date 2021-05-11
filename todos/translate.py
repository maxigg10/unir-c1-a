import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')

def get (event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    source_languague = "auto"
     if event['pathParameters']['lang'] == 'en':
         target_language = 'en'
     elif event['pathParameters']['lang'] == 'fr':
         target_language = 'fr'
     else:
         target_language = 'auto'

    finalresult=translate.translate_text(Text=result['Item']['text'], SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    result['Item']["text"] = finalresult.get('TranslatedText')

    #create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

   # return response
