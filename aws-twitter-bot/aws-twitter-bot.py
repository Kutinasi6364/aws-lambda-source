import tweepy

# Twitter APIキーとアクセストークン
API_KEY = 'lwK3xV0teLNwOhN2TvHqZ5Ilj'
API_SECRET_KEY = '8KcVkuiR6S5ZOePmiYnHGsFDIdcmvQi3WcLm6kbvXkN9eDT0gI'
ACCESS_TOKEN = '1526133517498736640-3dmCYB7C1cNQz7ksujXRYvKt414NLm'
ACCESS_TOKEN_SECRET = 'Fy3wY4fN6MheWLQFZfw1C0SBeUXpA1xTkFomVcYcJhhxK'

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
