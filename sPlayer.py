#!/usr/bin/python3

import ctypes, os, platform, sys, time, threading, random, yt_search, simpleaudio

# YouTube Search API v3에 대응하는 API 키를 편의상 일부러 깠습니다
# 원하시면 바꾸셔도 됩니다
yt = yt_search.build('AIzaSyD6UTc45CgZoComo_Abqu7jL16YjXhTurA')

songs = []
songs_dl = []
ap = True

print("YTSongsBot v 1.10")
print("type 'h' for help")

def sys_search_video(title):
    print("Search result of keyword " + title)
    print("select a number in search list")
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
    osis = platform.system()
    if osis == "Windows":
        trashbin = ">NUL"
    elif osis == "Linux":
        trashbin = ">/dev/null"
    else:
        trashbin = ""
    os.system('youtube-dl -x --audio-format=wav --output "' + vid + '.%(ext)s" https://www.youtube.com/watch?v=' + vid + trashbin)

def sys_AudioPlayer():
    TitlenoLoop = 0
    global songs_dl
    global ap
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
                TitlenoLoop = 0
                ctypes.windll.kernel32.SetConsoleTitleW("▶ " + np[0])
                wave_obj = simpleaudio.WaveObject.from_wave_file(np[1] + '.wav')
                play_obj = wave_obj.play()
                play_obj.wait_done()
                os.remove(np[1] + '.wav')
        time.sleep(.5)

def sys_AutoDownloader():
    global songs
    global songs_dl
    while 1 == 1:
        if not songs:
            pass
        else:
            if os.path.isfile(songs[0][1] + ".wav"):
                pass
            else:
                sys_DownloadSong(songs[0][1])
            songs_dl.append(songs[0])
            del songs[0]
        time.sleep(.5)

t = threading.Thread(target=sys_AudioPlayer)
t.start()

t2 = threading.Thread(target=sys_AutoDownloader)
t2.start()

while 1 == 1:
    inp = input(">")
    if inp == "h":
        print("h            : this help")
        print("r (keyword)  : search song and add to playlist")
        print("l            : print playlist")
        print("sf           : shuffle playlist")
        print("del (number) : delete item in playlist")
        print("pr (number)  : priorite playlist item to next song")
        print("sk           : skip current song")
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
        pn = 0
        if not songs_dl and not songs:
            print("no song in playlist")
        else:
            for p in songs_dl:
                print("#" + str(pn) + " : " + p[0])
                pn += 1
        if not songs:
            pass
        else:
            for q in songs:
                print("#" + str(pn) + " : " + q[0] + " (Downloading in progress)")
                pn += 1
    elif inp == "sf":
        random.shuffle(songs_dl)
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
    elif inp == "sk":
        simpleaudio.stop_all()
    else:
        continue