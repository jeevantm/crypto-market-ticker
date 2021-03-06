import tweepy
import requests
import json


def authenticate(data):

    access_token = data["access_token"]
    access_token_secret = data["access_token_secret"]
    consumer_token = data["consumer_token"]
    consumer_token_secret = data["consumer_token_secret"]

    auth = tweepy.OAuthHandler(consumer_token, consumer_token_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def max_value(inputlist):
    return max([sublist[-1] for sublist in inputlist])


def koinex_ticker(data):
    koinex_inr = []

    koinex_coin_fetch_list = data["koinex_coin_fetch_list"]

    result = requests.get('https://koinex.in/api/ticker').json()

    inr_prices = result["prices"]["inr"]

    for coin in koinex_coin_fetch_list:
        koinex_inr.append([coin.upper(), float(inr_prices[coin.upper()])])

    return koinex_inr


def wazirx_ticker(data):
    wazirx_inr = []
    wazirx_coin_fetch_list = data["wazirx_coin_fetch_list"]

    result = requests.get('https://api.wazirx.com/api/v2/tickers').json()

    for coin in result:
        if coin.lower().endswith('inr') and coin[:-3].lower() in wazirx_coin_fetch_list:
            wazirx_inr.append([result[coin]["base_unit"].upper(), result[coin]["last"]])

    return wazirx_inr


def coinmarketcap_ticker(data):
    coinmarketcap_inr = []
    coinmarketcap_coin_fetch_list = data["coinmarketcap_coin_fetch_list"]
    coinmarketcap_secret_token = data["coinmarketcap_secret_token"]

    result = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='+coinmarketcap_coin_fetch_list+'&convert=INR', headers={"X-CMC_PRO_API_KEY":coinmarketcap_secret_token}).json()

    for coin in result["data"]:
        coinmarketcap_inr.append([coin, '{0:.1f}'.format(result["data"][coin]["quote"]["INR"]["price"])])

    return coinmarketcap_inr


def build_tweet_body(koinex_inr, wazirx_inr, coinmarketcap_inr):
    body = "\nKOINEX (@koinexindia)\n"
    for kcoin in sorted(koinex_inr):
        body = body + str(kcoin[0]) + ":" + str(kcoin[1]) + "\n"

    body = body + "\nWAZIRX (@WazirXIndia)\n"
    for wcoin in sorted(wazirx_inr):
        body = body + str(wcoin[0]) + ":" + str(wcoin[1]) + "\n"

    body = body + "\nCOINMARKETCAP (@CoinMarketCap)\n"
    for ccoin in sorted(coinmarketcap_inr):
        body = body + str(ccoin[0]) + ":" + str(ccoin[1]) + "\n"

    # body = body + "\n#cryptocurrency #blockchain"

    return body

def main():
    with open('config.json', 'r') as config_file:
        data = json.load(config_file)

    api = authenticate(data)

    koinex_inr = koinex_ticker(data)
    wazirx_inr = wazirx_ticker(data)
    coinmarketcap_inr = coinmarketcap_ticker(data)

    body = build_tweet_body(koinex_inr, wazirx_inr, coinmarketcap_inr)
    header = "\n#Crypto Market Update (INR)\n"

    tweet = header + body

    api.update_status(tweet)


if __name__ == '__main__':
    main()