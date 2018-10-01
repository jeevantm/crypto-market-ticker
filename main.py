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
    # koinex_inr_stats = []
    koinex_coin_fetch_list = data["coin_fetch_list"]

    result = requests.get('https://koinex.in/api/ticker').json()

    inr_prices = result["prices"]["inr"]
    # inr_stats = result["stats"]["inr"]

    for coin in koinex_coin_fetch_list:
        koinex_inr.append([coin.upper(), float(inr_prices[coin.upper()])])
    #     koinex_inr_stats.append([coin.upper(), float(inr_stats[coin.upper()]["per_change"][:5])])
    #
    # maxc = max_value(koinex_inr_stats)
    #
    # for coin in koinex_inr_stats:
    #     if maxc in coin:
    #         best_returns_coin = coin
    #         break

    return koinex_inr


def wazirx_ticker(data):
    wazirx_inr = []
    wazirx_coin_fetch_list = data["coin_fetch_list"]

    result = requests.get('https://api.wazirx.com/api/v2/tickers').json()

    for coin in result:
        if coin.lower().endswith('inr') and coin[:-3].lower() in wazirx_coin_fetch_list:
            wazirx_inr.append([result[coin]["base_unit"].upper(), result[coin]["last"]])

    return wazirx_inr


def build_tweet_body(koinex_inr, wazirx_inr):
    body = "\nKOINEX (@koinexindia)\n"
    for kcoin in sorted(koinex_inr):
        body = body + str(kcoin[0]) + "  : " + str(kcoin[1]) + "\n"

    body = body + "\nWAZIRX (@WazirXIndia)\n"
    for wcoin in sorted(wazirx_inr):
        body = body + str(wcoin[0]) + "  : " + str(wcoin[1]) + "\n"

    return body

def main():
    with open('config.json', 'r') as config_file:
        data = json.load(config_file)

    api = authenticate(data)

    koinex_inr = koinex_ticker(data)
    wazirx_inr = wazirx_ticker(data)

    body = build_tweet_body(koinex_inr, wazirx_inr)
    header = "Market Update in INR\n"

    tweet = header + body
    api.update_status(tweet)


if __name__ == '__main__':
    main()