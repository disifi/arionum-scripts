import pandas as pd
import requests, json, time
import datetime

def masternode_block(x):
    mn_link = "http://"+x+"/api.php?q=currentBlock"
    try:
        r_mn = requests.get(mn_link,headers=header, timeout=timeout)
        block = json.loads(r_mn.content)["data"]["height"]
        print (x, block)
        return block
    except:
        print (x, "Unavailable")
        return 0

link = "http://62.210.169.171/api.php?q=masternodes"
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
r = requests.get(link, headers=header)
timeout = 3
masternodes = pd.DataFrame(json.loads(r.content)["data"]["masternodes"])
masternodes.rename(index=str, columns={"height": "Block_Registered"}, inplace = True)
start = time.time()

masternodes["Block_Current"] = masternodes.ip.apply(lambda x: masternode_block(x))
print("Took {} seconds\n".format(time.time()-start))
print ("Total number of registered MN:")
print(len(masternodes))
print()
print("Total count of the current blocks of the MNs:")
print(masternodes["Block_Current"].value_counts())
print()
print("Generated (UTC): ")
print(datetime.datetime.now())
