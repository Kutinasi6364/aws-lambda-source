import boto3
import ast
import tweepy
import datetime
from botocore.exceptions import ClientError

# SecretManager に設定したシークレット情報を取得する
def get_secret():
    
    # return はJson型を文字列にしているため
    
    secret_name = "twitter_bot_secret"
    region_name = "ap-northeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString'] # SecretString 内に入力したセキュリティ Key:Value が入っている
    return secret

def lambda_handler(event, context):
    secret = ast.literal_eval(get_secret()) # 文字列として格納されている→辞書型に変換
    
    # 各種変数をSecretManagerから取得
    API_KEY = secret["twitter_key"]
    API_KEY_SECRET = secret["twitter_key_secret"]
    TOKEN = secret["twitter_token"]
    TOKEN_SECRET = secret["twitter_token_secret"]
    
    client = tweepy.Client(None, API_KEY, API_KEY_SECRET, TOKEN, TOKEN_SECRET)

    # 投稿するテキスト
    tweet_text = "自動ツイート 現在時刻: " + str(datetime.datetime.now())

    # 投稿
    client.create_tweet(text=tweet_text)
    print(API_KEY +"  " +API_KEY_SECRET +"  "+ TOKEN +"  "+ TOKEN_SECRET)
    return secret

