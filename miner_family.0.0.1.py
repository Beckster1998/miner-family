import requests
from bs4 import BeautifulSoup
from pycoingecko import CoinGeckoAPI
from twilio.rest import Client
cg = CoinGeckoAPI()

#Twilio Input
account_sid = "AXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auth_token = "aXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client = Client(account_sid, auth_token)

#V.1 currently in prelim stage.

#CoinGecko is nice to provide a direct line to their data.

hush_cgk = str(cg.get_price(ids='hush', vs_currencies='btc'))
hush_cgk = hush_cgk.strip("'{}hush :btc")

#CoinMarketCap has an API system that I don't want to bother with at this time.
URL_cmc = 'https://coinmarketcap.com/currencies/hush/'
page_cmc = requests.get(URL_cmc)
soup_cmc = BeautifulSoup(page_cmc.content, 'html.parser')
results_cmc = soup_cmc.find('span', attrs={'class': 'cmc-details-panel-price__crypto-price'})
hush_cmc = results_cmc.get_text()
hush_cmc = hush_cmc.strip(" BTC")

#CoinPaprika has a dumb way of indexing their price but is manageable.
URL_cpp = 'https://coinpaprika.com/coin/hush-hush/'
page_cpp = requests.get(URL_cpp)
soup_cpp = BeautifulSoup(page_cpp.content, 'html.parser')
results_cpp = soup_cpp.find('span', attrs={'class': 'uk-display-block'})
hush_cpp = results_cpp.get_text()
hush_cpp = hush_cpp.splitlines()
hush_cpp = hush_cpp.pop(1)
hush_cpp = hush_cpp.strip(" BTC")

#Convert string to float.
hush_cgk = float(hush_cgk)
hush_cmc = float(hush_cmc)
hush_cpp = float(hush_cpp)

URL_miners = 'https://mining.luxor.tech/API/ZEN/user/Beckster/'
page_miners = requests.get(URL_miners).text
current = page_miners.find("hashrate_1h")
miners_rate = page_miners[(current+13):(current+24)]
miners_rate = float(miners_rate)
miner_hash = ["" , "" , ""]
j = 0
i = 0
for x in page_miners:
    j = page_miners.find("hashrate_five_min",(j+1),len(page_miners))
    if j == -1:
        break
    miner_hash[i] = page_miners[(j+19):(j+27)]
    i = i + 1

big_hash = float(miner_hash[0].rstrip(","))
lil_hash = float(miner_hash[1].rstrip(","))
jr_hash  = float(miner_hash[2].rstrip(","))
    


#Set desired notification price. For the time being, it will be 700 satoshi, AKA 10e-8 BTC, per HUSH.
dnp = 700e-08


sms_s = ""
sms = ""
xx = 0.0
if hush_cgk > dnp and hush_cmc > dnp and hush_cpp > dnp:
    sms_s = "Look on Graviex and sell your Hush! https://graviex.net/markets/hushbtc"
    xx = 1.0
if miners_rate < 200000.00:
    xx = 2.0
    sms = "Hashrate below 200 ksol/s. Check that it isn't a fluke: https://mining.luxor.tech/en/user/ZEN/Beckster"
    if big_hash < 105000.00:
        sms = "BigB is being odd. https://mining.luxor.tech/en/user/ZEN/Beckster"
        if lil_hash < 40000.00:
            sms = "BigB and LilB are being odd. https://mining.luxor.tech/en/user/ZEN/Beckster"
            if jr_hash < 40000.00:
                sms = "Someone has messed with the entire family. https://mining.luxor.tech/en/user/ZEN/Beckster"
    elif lil_hash < 40000.00:
        sms = "LilB is being odd. https://mining.luxor.tech/en/user/ZEN/Beckster"
        
        if jr_hash < 40000.00:
            sms = "LilB and JrB are being odd. https://mining.luxor.tech/en/user/ZEN/Beckster"
    elif jr_hash < 40000.00:
        sms = "JrB is being odd. https://mining.luxor.tech/en/user/ZEN/Beckster"
if xx == 1.0:        
    message = client.messages.create(
        to = "+1XXXxxxXXXX", #Desired number being sent to.
        from_ = "+1XXXxxxXXXX", #Twilio-Provided Number.
        body = sms_s)
    print(message.sid)
elif xx == 2.0:
    message = client.messages.create(
        to = "+1XXXxxxXXXX", #Desired number being sent to.
        from_ = "+1XXXxxxXXXX", #Twilio-Provided Number.
        body = sms)
    print(message.sid)
