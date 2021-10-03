import requests

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = 'caa8a3621a5e481c96807e77fe1dfc91'
news_params = {
    'q': "Tesla Inc",
    'apiKey': NEWS_API_KEY
}

response = requests.get(url=NEWS_ENDPOINT, params=news_params)
response.raise_for_status()
data = response.json()["articles"]

article = []
for i in range(3):
    article.append(data[i])

print(article)
