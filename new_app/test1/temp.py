import sys
import json
f=open("data.json","w")

root = {}
root["isleaf"]=False
root["children"]={}

print root
json.dump(root,f)
f.close()
