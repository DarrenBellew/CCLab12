import requests
import boto

res = requests.get('http://ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81/key')
keyId, key = res.text.split(":")


print(keyId)
print(key)
print(boto.Version)
