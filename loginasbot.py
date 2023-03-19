import tkinter, pywebview, os, re, json, time, main, subprocess
from urllib.request import Request, urlopen

print("Starting...")
i = input("What is your bot token? Please paste it in: ")
try:
  print(main.getBotByToken(i))
  print(f"Logging in as {main.getBotByToken(i)['name']}...")
except: print("We encountered an error during the account information retrieval process."); exit();

window = tkinter.Tk()

window.mainloop()
