import google_play_scraper as gps
import pandas as pd
import numpy as np
import json
import sys
play = pd.read_csv("apps.csv", sep = ",")
size = len(play)
window_size = size//1000
j = int(sys.argv[1])
end = int(sys.argv[2])
start = window_size*j
window_top = window_size + start
window_bottom = start
fail = 0
while j<end:
    j+=1
    play_sub = play.iloc[window_bottom:window_top]
    play_sub = play_sub.reset_index(drop = True)

    play_sub["Permissions"] = [None]*len(play_sub)
    fail=0 
    for i, app in enumerate(play_sub["App Id"]):       
        try:
            permission = gps.permissions(app_id = app)
            if type(permission) == dict:
                play_sub.at[i, "Permissions"] = json.dumps(permission)
            else:
                play_sub.at[i, "Permissions"] = permission
        except:
            fail+=1
    play_sub.to_csv("Permissions_New/Permission"+str(j)+".csv", index = False)
    window_bottom = window_top
    window_top += window_size