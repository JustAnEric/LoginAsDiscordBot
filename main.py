import os, re, json, time, subprocess
from json import loads, dumps
from urllib.request import Request, urlopen

def getBotByToken(token=None):
  if token:
    return loads(urlopen(Request("https://discord.com/api/v6/users/@me", headers={"Bearer Authorization": token})).read().decode())
  else: return print("Please specify a bot token that the program can get information from.")
