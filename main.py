import requests
import datetime as dt
import smtplib
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = 'OHPZ74YSUHS47RN2'
NEWS_API_KEY = 'caa8a3621a5e481c96807e77fe1dfc91'

USER = os.environ.get("EMAIL_USER")
PASS = os.environ.get("EMAIL_PASSWORD")

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'IBM',
    'apikey': STOCK_API_KEY
}

news_params = {
    'q': "Tesla Inc",
    'apiKey': NEWS_API_KEY
}

utc_time = dt.datetime.utcnow().date()
today_date = utc_time - dt.timedelta(days=1)
yesterday_date = str(today_date - dt.timedelta(days=2))
previous_day_date = str(today_date - dt.timedelta(days=3))

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()

data = response.json()

yesterday_close_price = int(float(
    data['Time Series (Daily)'][yesterday_date]['4. close']))
previous_day_close_price = int(float(
    data['Time Series (Daily)'][previous_day_date]['4. close']))

difference = abs(yesterday_close_price - previous_day_close_price)
difference_percent = (difference / yesterday_close_price) * 100

print(difference_percent)

if difference_percent > 5:
    response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    data = response.json()["articles"]

    article = []
    for i in range(3):
        article.append(data[i])

    connection = smtplib.SMTP(host="smtp.gmail.com")
    connection.starttls()
    connection.login(USER, PASS)
    for article in article:
        connection.sendmail(
            from_addr=USER,
            to_addrs=USER,
            msg=f"Subject:{STOCK}: {difference_percent} \n\n{article}"

        )

    print(data)
    print("Get News")


# STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.


# STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
# HINT 1: Think about using the Python Slice Operator


# STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
# HINT 1: Consider using a List Comprehension.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
