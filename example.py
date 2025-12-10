import gaybro
import requests
import json
import re
import random
import time


def youtube(args):
    args = args.replace(" ", "+")
    r = requests.get("https://www.youtube.com/results?search_query=" + args)
    r = re.findall(r'{"videoRenderer":{"videoId":"(.*?)","thumbnail":(.*?),"title":{"runs":(.*?),"accessibility":{"accessibilityData":{"label":"(.*?)"}}},"longBylineText":(.*?),"publishedTimeText":(.*?),"lengthText":{"accessibility":{"accessibilityData":{"label":"(.*?)"}},"simpleText":"(.*?)"},"viewCountText":{"simpleText":"(.*?)"},"navigationEndpoint"', r.text)

    j = (
            '{"videoRenderer":{"videoId":"%s","thumbnail":%s,"title":{"runs":%s,"accessibility":{"accessibilityData":{"label":"%s"}}},"longBylineText":%s,"publishedTimeText":%s,"lengthText":{"accessibility":{"accessibilityData":{"label":"%s"}},"simpleText":"%s"},"viewCountText":{"simpleText":"%s"}}}'
            % r[0]
        )
    d = json.loads(j)["videoRenderer"]
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

        return (e, r.json()["files"])
        
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

        if message[0] == "!":
            cmds = message[1:].split(" ", 1)
            if len(cmds) >1:
                cmd, args = cmds
            else:
                cmd, args = cmds[0], ""

        if cmd == "cmds":
            group.message("!yt, !sfw, !say")

        if cmd == "sfw":
            m, l = waifupics(args)
            group.message(m, l[0:4])

        if cmd == "say":
            if args:
                group.message(args)
            
        if cmd == "yt":
            t, l = youtube(args)
            group.message("%s @%s" % (t, user), l)

if __name__ == "__main__":
    #this will connect you to https://www.chatbro.com/en/186jN/
    #Gay.easy_start_non_block(["186jN"], "HentaiUwU")
    Gay.easy_start(["https://www.chatbro.com/en/186jN"], "HentaiUwU")
    #print(youtube("naruto"))
    
