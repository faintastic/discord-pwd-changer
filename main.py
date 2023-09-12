"""
██╗  ██╗ ██████╗ ██╗   ██╗ █████╗    ██████╗ ██╗██████╗ 
██║ ██╔╝██╔═══██╗██║   ██║██╔══██╗   ██╔══██╗██║██╔══██╗
█████╔╝ ██║   ██║██║   ██║███████║   ██████╔╝██║██████╔╝
██╔═██╗ ██║   ██║╚██╗ ██╔╝██╔══██║   ██╔══██╗██║██╔═══╝ 
██║  ██╗╚██████╔╝ ╚████╔╝ ██║  ██║██╗██║  ██║██║██║     
╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝     
                                                        
- Discord Password Changer
"""

from colorama import Fore, Style, init
from datetime import datetime
import time
import os
import ctypes
import random
import string
import tls_client
import threading

s = Fore.LIGHTBLUE_EX
r = Fore.WHITE
init(convert=True)

class Logger:
    def Sprint(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        print(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)
    
    def Ask(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)

class Changer:
    def __init__(self, new_pw: str = None):
        self.new_pw = new_pw
        self.tokens = []
        with open("input.txt", "r", encoding="utf-8") as file:
            for line in file:
                cleaned_line = line.strip()  
                if cleaned_line:
                    self.tokens.append(cleaned_line)
        self.session = tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True)
        self.Main()

    def Cookie(self):
        rq = self.session.get("https://discord.com")
        cookie = rq.cookies.get_dict()["locale"] = "us"
        return cookie
    
    def Finger(self, headers):
        rq = self.session.get("https://discordapp.com/api/v9/experiments", headers=headers).json()
        return rq["fingerprint"]
    
    def Change(self, token: str):
        headers2 = {'accept':'*/*','authority':"discord.com",'method':'POST','path':'/api/v9/auth/register','scheme':'https','origin':"discord.com",'referer':'discord.com/register','x-debug-options':'bugReporterEnabled','accept-language':'en-US,en;q=0.9','connection':'keep-alive','content-Type':'application/json','user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36','x-super-properties':'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjIwMDAiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTA0OTY3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin', 'Cookie': f"locale=us; {Changer.Cookie(self)}"}
        headers1 = {'x-super-properties':'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkzLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTMuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTAwODA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==','sec-fetch-dest':'empty','x-debug-options':'bugReporterEnabled','sec-fetch-mode':'cors','sec-fetch-site':'same-origin','accept':'*/*','accept-language':'en-GB','user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36','TE':'trailers','referer':'https://discord.com/channels/@me','authorization':token.split(':')[2],'x-fingerprint':Changer.Finger(self,headers2)}
        if self.new_pw is None: pw = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
        else: pw = self.new_pw

        payload = {
            "new_password": pw,
            "password": token.split(":")[1]
        }

        rq = self.session.patch("https://discord.com/api/v9/users/@me", headers=headers1, json=payload)
        if rq.status_code == 200:
            new = rq.json()["token"]
            Logger.Sprint("CHANGED", f"Changed token {s}old_token={r}{token.split(':')[2][:25]}***** {s}new_token={new[:25]}***** {s}new_pw={r}{pw}", Fore.GREEN)
            save = open("output.txt", "a")
            save.write(f"{token.split(':')[0]}:{pw}:{new}\n")
            save.close()
        else:
            Logger.Sprint("FAILED", f"Failed to change token password {s}token={r}{token.split(':')[2][:25]}*****", Fore.RED)
        
    def Main(self):
        ctypes.windll.kernel32.SetConsoleTitleW("Token Changer | Developed by kova / api")
        start = time.time()
        threads = []
        for i in range(len(self.tokens)):
            t = threading.Thread(target=self.Change, args=(self.tokens[i], )) 
            t.daemon = True
            threads.append(t)

        for i in range(len(self.tokens)):
            threads[i].start()
            time.sleep(.5)
        
        for i in range(len(self.tokens)):
            threads[i].join()
        
        end = time.time()
        with open("input.txt", "a") as file:
            file.truncate(0)
            file.close()
        elapsed = round(end - start, 2)
        Logger.Sprint("FINISHED", f"Finished changing tokens {s}elapsed={r}{elapsed}s", Fore.YELLOW)
        
        Logger.Ask("EXIT", "Please press the \"Enter\" key to close the application", Fore.MAGENTA)
        os._exit(1)

if __name__ == "__main__":
    new = Logger.Ask("CONFIG", "Please enter your new pw, if you want it to be auto generated, just click \"Enter\": ", Fore.YELLOW)
    if new == "": new = None
    Changer(new)