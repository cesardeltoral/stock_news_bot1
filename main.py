import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "******************"
NEWS_API_KEY = "******************"
TWILIO_SID = "*******************"
TWILIO_AUTH_TOKEN = "*******************"


requests.get(STOCK_ENDPOINT)

# yesterday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [values for (key, values) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
#the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)
#the positive difference between 1 and 2
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "⬇"

#the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 5:
    print("Get News")


#the News API to get articles related to the COMPANY_NAME.
if diff_percent > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# first 3 articles.
    three_articles = articles[:3]
    print(three_articles)


    #first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    #Sending each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message= client.messages.create(
            body=article,
            from_="*************",
            to="************"
        )


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""