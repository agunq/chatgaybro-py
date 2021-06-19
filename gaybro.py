#authot github @agunq (im not gay :v)

import time
import re
import json
import random
import base64

from threading import Thread

#pip install requests
#pip install websocket-client
import requests
import websocket

def strip_html(msg):
    msg = re.sub("<\/?[^>]*>", "", msg)
    return msg


class Group:

    def __init__(self, mgr, group):
        self._mgr = mgr
        self._group = group
        self._token = None
        self._csrfToken = None
        self._signature = None
        self._clientId = None
        self._chatId = None
        self._userId = None

        self.counter = 0
        self.title = ""
        self.group = group

        self._getCsrfToken()
        self._getClientId()
        self._getChatId()
        

    def disconnect(self):
        self._websock.close()

    def connect(self):
        
        self._websock = websocket.WebSocketApp("wss://ws.chatbro.com/ws?chatId=%s&clientId=%s" % (self._chatId, self._clientId), on_message=self._on_message)
        self._run_th()
        self._getToken()
        self.loginAnon(self._mgr._anonName)

    def _run(self):
        self._websock.run_forever(origin = "https://chatbro.com/")
        
    def _run_th(self):
        self.thread = Thread(target = self._run, args = ())
        self.thread.setDaemon(True)
        self.thread.start()

    def _callEvent(self, evt, *args, **kw): 
        getattr(self._mgr, evt)(self, *args, **kw)

    def _on_message(self, websock, message):
        data = json.loads(message)

        
        if data["type"] == "loginMe":
            self._userId = data["user"]["id"]
        
        if data["type"] == "count":
            self.counter = data["counters"][0]
            
        if data["type"] == "messageReceived":
           _data = strip_html(data["html"])[9:].split("         ", 1)
           user = _data[0]
           msg = _data[1][:-1]
           if msg[0] == " ":
               msg = msg[1:]
           
           self._callEvent("onMessage", user, msg)

           #print(self._userId)
               
    def _getClientId(self):
        self._clientId = float("0." + str(random.randint(10 ** 15, 10 ** 16)))

        
    def _getChatId(self):
        params = {"embedChatsParameters":
                  [{"encodedChatId":self._group,
                    "containerDivId":"chat",
                    "allowMoveChat":False,
                    "allowMinimizeChat":False,
                    "chatState":"maximized",
                    "siteDomain":"chatbro.com",
                    "chatHeight":"100%",
                    "chatWidth":"100%",
                    "allowUploadFile":True,
                    "signature":self._signature}],
                  "lang":"en-US",
                  "needLoadCode":True,
                  "embedParamsVersion":"8",
                  "chatbroScriptVersion":"a2e7f4b7eafef0c23e"}
        params = json.dumps(params)
        p = base64.b64encode(params.encode("ascii"))
        r = requests.get("https://www.chatbro.com/embed.js?" + p.decode("ascii"))
        
        chatid = re.search("\"chatId\": (.*?),", r.text)
        if chatid:
            self._chatId = int(chatid.group(1))
            print(self._chatId)
        

    def _getCsrfToken(self):
        h = requests.get("https://www.chatbro.com/en/" + self._group)
        if "Set-Cookie" in h.headers:
            cookie = h.headers["Set-Cookie"]
            token = re.search("csrfToken=(.*?);", cookie)
            if token:
                token = token.group(0)
                self._csrfToken = token
                #print(self._csrfToken)
                
        t = h.text
        loader = re.search("signature: '(.*?)'", t)
        if loader:
            self._signature = loader.group(1)
            
        title = re.search("<title> (.*?) </title>", t)
        if title:
            self.title = title.group(1)
            
                
    def _getToken(self):
        h = requests.get("https://www.chatbro.com/get_csrf_token/")
        if "Set-Cookie" in h.headers:
            cookie = h.headers["Set-Cookie"]
            token = re.search("JSESSIONID=(.*?);", cookie)
            if token:
                token = token.group(0)
                self._token = token
            #print(self._token)
            return token

    def loginAnon(self, name = "AnonUwU"):
    
        data = {"name": name,
                "clientId": self._clientId,
                "chatId": self._chatId,
                "cr": "https://www.chatbro.com/en/%s/" % self._group
                }
        headers = {"referer": "https://www.chatbro.com/en/%s/" % self._group,
                   "Cookie": "siteLanguage=EN; %s %s" % (self._token, self._csrfToken)}
        
        r = requests.get("https://www.chatbro.com/guest_login/", headers = headers, params = data)
       

    def message(self, msg, img = None):
        
        ti = int(time.time() * 1000)
        if img:
            img = img.split("//", 1)[1]
            att = [{"type":"photo","title":"","thumbnailPhotoUrl":"//" + img, "originalPhotoUrl":"//" + img}]
        else:
            att = []
        payload = {"encodedChatId":self._group,
                   "body":{"text":msg,"attachments": att},
                   "chatLanguage":"EN","siteDomain":"chatbro.com","timestamp": ti,
                   "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
                   "mobile":False,
                   "connType":"ws",
                   "ud": self._userId,
                   "authorChatClientId": self._clientId,
                   "signature":self._signature,"permissions":[]}
        
        r = requests.post('https://www.chatbro.com/send_message/', data=json.dumps(payload),
                          headers={"referer": "https://www.chatbro.com/en/%s/" % self._group,
                                    "Cookie": "siteLanguage=EN; %s %s" % (self._token, self._csrfToken)})

        if r.text != "{}":
            print(r.text)

class GayBro:

    def __init__(self, name = "AnonUwU"):
        self._groups = {}
        self._anonName = name
        
    @classmethod    
    def easy_start(cl, ids, name = "AnonUwU"):
        
        self = cl(name = name)
        for _id in ids:
            self.joinGroup(_id)

    def onMessage(self, group, user, msg):
        pass

    def joinGroup(self, _id):  
        if _id not in self._groups:
            self._groups[_id] = Group(mgr = self, group = _id)
            self._groups[_id].connect()

    def leaveGroup(self, _id):
        if _id in self._groups:
            self._groups[_id].disconnect()


