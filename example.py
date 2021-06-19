import gaybro
import requests
import json
import re
import random
import time


def youtube(args):
    args = args.replace(" ", "+")
    r = requests.get("https://www.youtube.com/results?search_query=" + args)
    r = re.findall('{"videoRenderer":(.*?)(false}]}|}]}}}]})', r.text)
    d = json.loads(r[0][0] + r[0][1])
    t = d["title"]["runs"][0]["text"]
    u = "https://youtu.be/" + d["videoId"]
    p = d["publishedTimeText"]["simpleText"]
    l = d["lengthText"]["simpleText"]
    v = d["viewCountText"]["simpleText"]
    return "%s \r | %s | %s | %s | %s" % (t, p, l, v, u), u

def waifupics(args):
    y = ["waifu","neko","shinobu","megumin","bully","cuddle","cry","hug","awoo","kiss","lick","pat","smug","bonk","yeet","blush","smile","wave","highfive","handhold","nom","bite","glomp","slap","kill","kick","happy","wink","poke","dance","cringe"]
    try:
        p = {"exclude":[""]}
        if args.lower() in y:
            e = args.lower()
        else:
            e = "waifu"
        h = {"referer": "https://waifu.pics/"}
        r = requests.post("https://api.waifu.pics/many/sfw/" + e, headers = h, data = p)
        
        return (e, r.json()["files"][0])
        
    except:
        return "please try another type: %s" % ", ".join(y), ""
    

    
class Gay(gaybro.GayBro):


    def onMessage(self, group, user, message):

        if user == group._mgr._anonName: return
        
        print(group.group, group.title, user, message)

        if message == "selamat pagi":
            r = ["pagi juga", "selamat pagi", "hai :d"]
            t = random.choice(r)
            group.message(t + " @%s" % user)

        if message[0] == ",":
            cmds = message[1:].split(" ", 1)
            if len(cmds) >1:
                cmd, args = cmds
            else:
                cmd, args = cmds[0], ""

        if cmd == "cmds":
            group.message("!yt, !sfw, !say")

        if cmd == "sfw":
            m, l = waifupics(args)
            group.message(m, l)

        if cmd == "say":
            if args:
                group.message(args)
            
        if cmd == "yt":
            t, l = youtube(args)
            group.message("%s @%s" % (t, user), l)

if __name__ == "__main__":
    Gay.easy_start(["186jN"], "HentaiUwU")
    
