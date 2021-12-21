import pandas as pd
import google_play_scraper as gps
import sys
play = pd.read_csv("/u/s/k/skruse/private/cs736/FinalProject/Google-Playstore-Dataset/dataset/Googple-Playstore-Dataset.csv", sep = ",")

results = []
failed = []
code = []
appids = play["App Id"].unique()
i = int(sys.argv[1])
windowSize = 500000
urls = []
for ap in appids[i:(i+windowSize)]:
    try:
        result = gps.app(
            ap,
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        
        url_dev = result["developerId"]
        url_str = "https://play.google.com/store/apps/developer?id="
        url_int = "https://play.google.com/store/apps/dev?id="
        if result["developerId"].isnumeric():
            url_dev = url_int + result["developerId"]
        else:
            url_dev = url_str + result["developerId"]

        success = urlopen(url_dev).getcode()

        results.append(url_dev)
        code.append(success)
    except Exception as e:
        code.append(e)
        results.append("FAIL:"+ap)

nums = len(results)
num2 = len(failed)
dif = nums - num2
failed.extend([None]*dif)
pd.DataFrame({"ids": results,"failed":failed, "code": code}).to_csv("devs/devIds"+str(i) +".csv", index = False)