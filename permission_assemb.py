import pandas as pd
import json
import os.path
import collections
import sys
buckets = collections.defaultdict(collections.Counter)
names = pd.read_csv("Permissions_all.csv", index_col = 0, nrows = 1)
start = int(sys.argv[1])
df = pd.read_csv("Permissions_all.csv", index_col = 0, names = names.columns, skiprows = start, nrows = 500000)
df = df.reset_index(drop = True)
for i,perm in enumerate(df["Permissions"]):
    if type(perm) == str:
        df.at[i,"Permissions"] = json.loads(perm)

for perm in df["Permissions"]:
    if type(perm) == dict:
        for _type, value in perm.items():
            buckets[_type].update(value)
for key in buckets.keys():
    df[key] = [None]*len(df["App Id"])
                
for app in range(len(df["App Id"])):
    if type(df["Permissions"][app]) == dict:
        for ptype, vals in df["Permissions"][app].items():
            df[ptype][app] = vals
            
df.to_csv("permissions_columns/perm"+str(start)+".csv", index = False)