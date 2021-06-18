import gaybro

class Gay(gaybro.GayBro):


    def onMessage(self, group, user, message):
        
        print(group._group, user, message)
        
        if message == "selamat pagi":
            group.message("pagi juga gay @%s" % user)

if __name__ == "__main__":
   
    Gay.easy_start(["186jN"], "hentai")
