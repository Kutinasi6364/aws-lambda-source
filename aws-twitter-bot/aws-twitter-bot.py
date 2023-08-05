import boto3
import ast
import tweepy
import requests
import pytz
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError


def get_secret():
    """AWS SecretManager取得
    Overview:
        AWS SecretManager からシークレット情報を取得
    Raises:
        e: SecretManager 接続エラー出力用
    Returns:
        secret (str): json形式の文字列(辞書型に変更必要)
    """

    secret_name = "twitter_bot_secret"
    region_name = "ap-northeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        raise e

    # SecretString 内に入力したセキュリティ Key:Value が入っている
    secret = get_secret_value_response['SecretString']
    return secret


def scrape_article():
    """スクレイピング実行
    Overview:
        指定したサイトの記事タイトルと記事URLを取得
    Args:
        url (str): 記事を検索するサイトURL
    Returns:
        article_title (str): 記事タイトル
        link_url (str): 記事URL
    """
    # file_path = "VTuber-MoguLive.html" # ローカルのHTMLファイルパスを指定
    # # ファイルを読み込んでBeautifulSoupオブジェクトを作成
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     html = file.read()
    # soup = BeautifulSoup(html, 'html.parser')

    url = "https://www.moguravr.com/category/virtual-youtuber/"  # スクレイピングを行うURL

    # HTTPリクエストを送信してHTMLコンテンツを取得
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    # Beautiful Soupを使ってHTMLを解析
    soup = BeautifulSoup(response.content, 'html.parser')

    # 記事の本文を抽出
    article_elements = soup.find('h3')  # 本文は h3 に記載されている
    article_title = article_elements.get_text()  # テキストのみ抜き出し(本文)

    class_element = soup.find(class_="mt-3 mt-xl-4")  # URL 直近のクラス範囲取得
    if class_element:
        first_element = class_element.find('a')  # a タグ内の要素取得
    if first_element:
        link_url = first_element['href']  # href 要素抜き出し

    return article_title, link_url


def aws_tweet_bot(event, context):
    """自動ツイート

    Overview:
        スクレイピングで取得した記事本文と記事URLを自動投稿する
    Args:
        event (dummy): lambda 特殊引数
        context (dummy): lambda 特殊引数
    Returns:
        secret: シークレット情報(確認用)
    """
    secret = ast.literal_eval(get_secret())  # 文字列として格納されている→辞書型に変換

    # 各種変数をSecretManagerから取得
    API_KEY = secret["twitter_key"]
    API_KEY_SECRET = secret["twitter_key_secret"]
    TOKEN = secret["twitter_token"]
    TOKEN_SECRET = secret["twitter_token_secret"]

    client = tweepy.Client(None, API_KEY, API_KEY_SECRET, TOKEN, TOKEN_SECRET)

    # 投稿するテキスト
    now = datetime.now(tz=timezone.utc)
    time_zone = pytz.timezone("Asia/Tokyo")
    jpn_now = time_zone.normalize(now.astimezone(time_zone))  # 日本時間に変換(元UTC)
    article_title, link_url = scrape_article()  # スクレイピング結果を取得 本文, リンクURL
    tweet_text = "\n".join(["最新記事: ", article_title, link_url, str(jpn_now)])

    # 投稿
    client.create_tweet(text=tweet_text)
    print(" ".join([API_KEY, API_KEY_SECRET, TOKEN, TOKEN_SECRET]))
    return secret


# if __name__ == "__main__":
    # aws_tweet_bot("dummy1", "dummy2")
