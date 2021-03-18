import requests
import os
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")


params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT,params=params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
stocks_data = [value for(key,value)in data.items()]

yesterday_stock_price = float(stocks_data[0]['4. close'])
before_yesterday_stock_price = float(stocks_data[1]['4. close'])

up_down = None

difference_data = yesterday_stock_price-before_yesterday_stock_price
if difference_data > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_change = round((difference_data/yesterday_stock_price)*100)
if abs(percentage_change) > 5:
    params={
        "qInTitle":COMPANY_NAME,
        "apikey":NEWS_API_KEY,
    }
    news_response = requests.get(url=NEWS_ENDPOINT,params=params)
    news_response.raise_for_status()
    data_articles = news_response.json()["articles"]
    three_articles = data_articles[:3]

    formatted_articles = [f"{STOCK_NAME}:{up_down}{percentage_change}%\nHeadline:{article['title']}.\nBreif:{article['description']}" for article in three_articles]


    account_sid = os.environ.get("account_sid")
    auth_token = os.environ.get("auth_token")
    client = Client(account_sid,auth_token)

    for article in formatted_articles:
        message = client.messages\
            .create(
            body=article,
            from_=os.environ.get("from_"),
            to=os.environ.get("to")
        )
        print(message.status)


