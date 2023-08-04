import tweepy

# Twitter APIキーとアクセストークン
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = '-'
ACCESS_TOKEN_SECRET = ''

def lambda_handler(event, context):
    try:
        # Tweepyを初期化
        auth = tweepy.Client(None, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        # api = tweepy.API(auth)

        # 投稿するテキスト
        tweet_text = "これは自動投稿のテストです。Hello, Twitter from AWS Lambda!"

        # 投稿
        auth.create_tweet(text=tweet_text)

        return {
            'statusCode': 200,
            'body': '投稿が成功しました。'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
