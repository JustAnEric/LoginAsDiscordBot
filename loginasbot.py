import tkinter, os, re, json, time, subprocess, flask
from json import loads, dumps
from urllib.request import Request, urlopen

def getBotByToken(token=None):
  if token:
    return loads(urlopen(Request("https://discord.com/api/v6/users/@me", headers={"Bearer Authorization": token})).read().decode())
  else: return print("Please specify a bot token that the program can get information from.")


print("Starting...")
i = input("What is your bot token? Please paste it in: ")
try:
  print(getBotByToken(i))
  print(f"Logging in as {getBotByToken(i)['name']}...")
except: print("We encountered an error during the account information retrieval process."); exit();

load = flask.Flask('server')
@load.route('/')
def home():
  return flask.redirect("/login")

@load.route('/login')
def login_as_discord_bot():
  return flask.render_template('login.html')

load.run(port=8080)