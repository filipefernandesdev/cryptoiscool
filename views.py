from flask import Blueprint, render_template, request
from binance.spot import Spot
from datetime import datetime, timedelta
import requests
import json
views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/crypto")
def get_all_prices():
    # Query Parameters
    args = request.args
    quoteAsset = args.get("q")
    if quoteAsset == None:
        quoteAsset = "EUR"

    # Binance Library
    client = Spot()

    # Available baseAssets
    baseAsset = ["BTC", "ETH", "XRP", "BNB", "XLM"]

    # Cryptos
    symbol = []
    for i in baseAsset:
        symbol.append(i+quoteAsset)

    # Current Price
    price = []
    for i in symbol:
        price.append(float((client.ticker_price(i))["price"]))

    # Price 24 hours (%)
    price24h = []
    for i in symbol:
        price24h.append(float((client.ticker_24hr(i))["priceChangePercent"]))

    return render_template("crypto.html", baseAsset=baseAsset, quoteAsset=quoteAsset, symbol=symbol, price=price, price24h=price24h)


@views.route("/crypto/<baseAsset>")
def get_specific_data(baseAsset):
    # Query Parameters
    args = request.args
    quoteAsset = args.get("q")
    if quoteAsset == None:
        quoteAsset = "EUR"

    # Symbol
    symbol = baseAsset + quoteAsset

    # Binance Library
    client = Spot()

    # Current Price
    price = float((client.ticker_price(symbol))["price"])

    # Price 24 hours (%)
    price24h = float((client.ticker_24hr(symbol))["priceChangePercent"])

    # Price History - 2-week - daily
    priceHistory = (client.klines(symbol, "1d", limit=14))
    priceHistory_open = []
    priceHistory_high = []
    priceHistory_low = []
    priceHistory_close = []

    for day in priceHistory:
        priceHistory_open.append(float(day[1]))
        priceHistory_high.append(float(day[2]))
        priceHistory_low.append(float(day[3]))
        priceHistory_close.append(float(day[4]))

    # Date
    dateList = []
    for i in range(1, 15):
        currentDate = datetime.today() - timedelta(days=i)
        formattedDate = currentDate.strftime('%d-%m-%Y')
        dateList.append(formattedDate)

    # NewsAPI
    newsapi_baseurl = "https://newsapi.org/v2/everything?language=en&searchIn=title"
    newsapi_key = "a50b295bcc124951af8c25f798ef9303"

    if baseAsset == "BTC":
        newsapi_theme = "bitcoin"
    elif baseAsset == "ETH":
        newsapi_theme = "ethereum"
    elif baseAsset == "BNB":
        newsapi_theme = "'binance coin'"
    else:
        newsapi_theme = baseAsset

    newsapi_sortby = "popularity"

    newsapi_date = datetime.today() - timedelta(days=31)
    newsapi_dateFormatted = newsapi_date.strftime('%Y-%m-%d')

    newsapi_finalurl = newsapi_baseurl + "&from=" + newsapi_dateFormatted + \
        "&sortby=" + newsapi_sortby + "&q=" + newsapi_theme + "&apikey=" + newsapi_key

    newsapi_requestnews = requests.get(newsapi_finalurl)
    newsapi_getnews = json.loads(newsapi_requestnews.content)

    return render_template("crypto_specific.html", baseAsset=baseAsset, quoteAsset=quoteAsset, symbol=symbol, price=price, price24h=price24h, priceHistory_open=priceHistory_open, priceHistory_high=priceHistory_high, priceHistory_low=priceHistory_low, priceHistory_close=priceHistory_close, dateList=dateList, newsapi_getnews=newsapi_getnews)


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")
