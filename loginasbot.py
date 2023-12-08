import tkinter, os, re, json, time, subprocess, flask, requests, random
from json import loads, dumps
from urllib.request import Request, urlopen
from _options import *
from _terminal import *

user = {}
token = None
currServer = {}

def getBotByToken(token=None):
  if token:
    return (requests.get(f"https://discord.com/api/v{random.choice([8,9,10])}/users/@me", headers={"Authorization": "Bot "+token}).json())
  else: return print("Please specify a bot token that the program can get information from.")

def getBotServers():
  if token:
    return (requests.get(f"https://discord.com/api/v{random.choice([8,9,10])}/users/@me/guilds", headers={"Authorization": "Bot "+token}).json())
  else:
    return "ERROR_NO_TOKEN"
  
def getServerInfo(id:int):
  if token:
    for x in getBotServers():
      if int(x['id']) == int(id):
        u = requests.get(f"https://discord.com/api/v{random.choice([8,9,10])}/guilds/{x['id']}", headers={"Authorization": "Bot "+token}).json()
        return {"fromraw":x,"frombot":u}
    return "UNKNOWN_GUILD"
  else:
    return "ERROR_NO_TOKEN"
  
def getChannelsInServer(server):
  channels = requests.get(f"https://discord.com/api/v{random.choice([8,9,10])}/guilds/{server['id']}/channels", headers={"Authorization": "Bot "+token}).json()
  return channels

def getServerInvites(server):
  invites = requests.get(f"https://discord.com/api/v{random.choice([8,9,10])}/guilds/{server['id']}/invites", headers={"Authorization": f"Bot {token}"}).json()
  return invites

print("Starting...")
i = input("What is your bot token? Please paste it in: ")
try:
  print(getBotByToken(i))
  print(f"Logging in as {getBotByToken(i)['username']}...")
  token = i
except: print("We encountered an error during the account information retrieval process."); exit()

print("")
options = [
  "Text version",
  "Browser version (incomplete)"
]
txtopts = create_text_options(options)
print(txtopts)
inp = int(input('(0,1) '))

if get_option_answer(txtopts, inp) == options[1]:
  load = flask.Flask('server')
  @load.route('/')
  def home():
    return flask.redirect("/login")

  @load.route('/login')
  def login_as_discord_bot():
    return flask.render_template('login.html')

  load.run(port=8080)
elif get_option_answer(txtopts, inp) == options[0]:
  # enter text version
  clear()
  user = getBotByToken(token)
  sopts = [x['name']+" ^({})^".format(x['id']) for x in getBotServers()]
  servertxtoptions = create_text_options(sopts)
  print(f"""
  {user['username']}#{user['discriminator']}
  ----------------------------------------------------------------------------------------------------------------------------------------
  {user['bio']}
  Servers:--------------------------------------------------------------------------------------------------------------------------------
{servertxtoptions}

""")
  i = input(f"(0-{len(servertxtoptions.split(newline()))-1}) ") #numbers
  if in_range(int(i), len(servertxtoptions.split(newline()))-1):
    print(f"Looking in index ({i})")
    ind = get_option_answer(servertxtoptions, i)
    print(ind)
    print(f"Grabbing server information for {ind.split('^(')[1].split(')^')[0]}")
    serverInfo = getServerInfo(int(ind.split('^(')[1].split(')^')[0]))['frombot']
    currServer = serverInfo
    clear()
    # print server information
    print(serverInfo)
    sopts = [f"({x['id']}) "+"#"+x['name'] for x in getChannelsInServer(serverInfo) if x['type'] == 0]
    channeltxtoptions = create_text_options(sopts)
    sopts2 = [f"({x['id']}) "+"🔊"+x['name'] for x in getChannelsInServer(serverInfo) if x['type'] == 2]
    vcchanneltxtoptions = create_text_options(sopts2)
    sopts4 = [f"({x['id']}) "+x['name'] for x in getChannelsInServer(serverInfo) if x['type'] == 4]
    gcchanneltxtoptions = create_text_options(sopts4)
    sopts5 = [f"({x['id']}) "+"📢"+x['name'] for x in getChannelsInServer(serverInfo) if x['type'] == 5]
    announcchanneltxtoptions = create_text_options(sopts5)
    print(f"""
  {user['username']}#{user['discriminator']}
  Server Invites: {getServerInvites(currServer)}
  Text Channels:--------------------------------------------------------------------------------------------------------------------------
{channeltxtoptions}
  Voice Channels:-------------------------------------------------------------------------------------------------------------------------
{vcchanneltxtoptions}
  Categories:-----------------------------------------------------------------------------------------------------------------------------
{gcchanneltxtoptions}
  Announcement Channels:------------------------------------------------------------------------------------------------------------------
{announcchanneltxtoptions}
""")
    run = True

    while run:
      i = input("(?/Action~Prompt) ")
      if i.lower() == "quit" or i.lower() == "close" or i.lower() == "stop":
        exit()
      elif i.startswith('view'):
        try:
          command = i.split(' ',1)[1]
        except: command = i
        if "category" in command:
          print("You cannot view a category.")
        elif "text" in command:
          print("You cannot view a text channel.")
        elif "voice" in command:
          print("You cannot view a voice channel.")
        elif "news" in command:
          print("You cannot view a news channel.")
        else:
          print("Error.")
else:
  print("Unknown option.")