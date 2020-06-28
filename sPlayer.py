# TODO : 
# BUG : 스킵 불가능

# Configuration
yt_apikey = 'AIzaSyD6UTc45CgZoComo_Abqu7jL16YjXhTurA'
# -----

import os, sys, time, threading, random, yt_search, configparser, ctypes
from playsound import playsound

yt = yt_search.build(yt_apikey)
log = configparser.ConfigParser()
log.read("cache.txt")

songs = []
songs_dl = []
ap = True

print("YTSongsBot v 0.51")
print("type 'h' for help")

ctypes.windll.kernel32.SetConsoleTitleW("■ Play anything you want")

def sys_search_video(title):
    search_result = yt.search(title, sMax=10, sType=["video"])
    ni = 0
    for i in search_result.title:
        print("#" + str(ni) + " : " + i + " by " + search_result.channelTitle[ni])
        ni += 1
    print("x  : cancel current search")
    while 1 == 1:
        inpa = input("N>")
        if inpa == "x":
            raise
        try:
            n = int(inpa)
            return [search_result.title[n], search_result.videoId[n], search_result.channelTitle[n]]
        except:
            continue

def sys_DownloadSong(vid):
    print("Downloading VID " + vid)
    os.system('youtube-dl -x --audio-format=wav --output "' + vid + '.%(ext)s" https://www.youtube.com/watch?v=' + vid + ">NUL")
    print("Download complete")
    print(">", end = "")

def sys_PlaySong(filename):
    print("Playing target media.")
    playsound(filename + '.wav')
    print("Completed playing target media.")

def sys_AudioPlayer():
    TitlenoLoop = 0
    global songs_dl
    global ap
    print("audio player service called")
    while 1 == 1:
        if not songs_dl:
            if TitlenoLoop >= 1:
                pass
            else:
                ctypes.windll.kernel32.SetConsoleTitleW("■ Play anything you want")
                TitlenoLoop += 1
        else:
            np = songs_dl[0]
            del songs_dl[0]
            if ap:
                print("now playing : " + np[0])
                TitlenoLoop = 0
                ctypes.windll.kernel32.SetConsoleTitleW("▶ " + np[0])
                sys_PlaySong(np[1])
        time.sleep(.5)

def sys_AutoDownloader():
    global songs
    global songs_dl
    print("auto downloader service called")
    songs_played = []
    ca = log.items("cache")
    for c in ca:
        songs_played.append(c[0])
    while 1 == 1:
        if not songs:
            pass
        else:
            if os.path.isfile(songs[0][1] + ".wav"):
                pass
            else:
                sys_DownloadSong(songs[0][1])
                log.set("cache", songs[0][1], songs[0][0])
                with open("cache.txt", 'w') as configfile:
                    log.write(configfile)
            songs_dl.append(songs[0])
            del songs[0]
        time.sleep(.5)

def Menu():
    global songs
    global songs_dl
    global ap
    global t
    print("Menu called")
    while 1 == 1:
        inp = input(">")
        if inp == "h":
            print("h            : this help")
            print("r (keyword)  : search song and add to playlist")
            print("l            : print playlist")
            print("sf           : shuffle playlist")
            print("sk           : skip current song")
            print("del (number) : delete item in playlist")
            print("pr (number)  : priorite playlist item to next song")
            print("----- do not procedure if you don't know what are you doing -----")
            print("ren          : rename cached wave files to its original name and clear cache")
            print("ap           : toggles audio player")
        elif inp.startswith("r") and inp != "ren":
            if inp == "r":
                print("Usage = r (search keyword)")
            else:
                keyword = inp.replace("r ", "")
                try:
                    result = sys_search_video(keyword)
                    songs.append(result)
                except:
                    continue
        elif inp == "l":
            if not songs_dl:
                print("no song in playlist")
            else:
                pn = 0
                for p in songs_dl:
                    print("#" + str(pn) + " : " + p[0])
                    pn += 1
        elif inp == "sf":
            random.shuffle(songs_dl)
        elif inp == "sk":
            t.terminate()
            t = threading.Thread(target=sys_AudioPlayer)
            t.start()
        elif inp.startswith("del"):
            if inp == "del":
                print("Usage : del (number)")
            else:
                try:
                    n = int(inp.replace("del ", ""))
                    del songs_dl[n]
                except:
                    print("invalid number")
        elif inp.startswith("pr"):
            if inp == "pr":
                print("Usage : pr (number)")
            else:
                try:
                    n = int(inp.replace("pr ", ""))
                    npr = songs_dl[n]
                    del songs_dl[n]
                    songs_dl.insert(0, npr)
                except:
                    print("invalid number")
        elif inp == "ren":
            it = log.items("cache")
            for i in it:
                os.rename(i[0] + ".wav", i[1] + ".wav")
                print(i[0] + "→" + i[1])
            log.remove_section("cache")
            log.add_section("cache")
            print("clearing cache")
            with open("cache.txt", 'w') as configfile:
                log.write(configfile)
        elif inp == "ap":
            if ap:
                ap = False
                print("audio player is OFF")
            else:
                ap = True
                print("audio player is ON")
        else:
            continue

t = threading.Thread(target=sys_AudioPlayer)
t.start()

t2 = threading.Thread(target=sys_AutoDownloader)
t2.start()

Menu()