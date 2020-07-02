#!/usr/bin/python3

import ctypes, os, platform, sys, time, threading, random, yt_search, simpleaudio, wave
from pypresence import Presence

# 사용자 편의를 위해 Youtube Data API v3에 대응하는 API Key를 일부러 깠습니다
# 원하신다면 바꾸셔도 됩니다
yt = yt_search.build('AIzaSyB586kMlriM12H1jYN8ZqNwd5RD-M79pjc')

songs = []
songs_dl = []
np = []
qp = False
hr = False
hr_enabled = True

RPC = None
try:
    RPC = Presence('726879500360482879')
    RPC.connect()
except:
    pass

osis = platform.system()

print("YTSongsBot v1.40")
print("type 'h' for help")

def sys_search_video(title):
    global qp
    print("Search result of keyword " + title)
    print("select a number in search list")
    search_result = yt.search(title, sMax=10, sType=["video"])
    if qp:
        print("added song " + search_result.title[0] + " by " + search_result.channelTitle[0] + ", now downloading")
        result = [search_result.title[0], search_result.videoId[0], search_result.channelTitle[0]]
    else:
        ni = 0
        for i in search_result.title:
            print("#" + str(ni) + " : " + i + " by " + search_result.channelTitle[ni])
            ni += 1
        print("x  : cancel current search")
        while 1 == 1:
            inpa = input("N>")
            if inpa == "x":
                raise
            else:
                try:
                    n = int(inpa)
                    result = [search_result.title[n], search_result.videoId[n], search_result.channelTitle[n]]
                    print("added song " + search_result.title[n] + " by " + search_result.channelTitle[n] + ", now downloading")
                    break
                except Exception as e:
                    print(e)
                    continue
        return result

def sys_DownloadSong(vid):
    global osis
    if osis == "Windows":
        os.system('youtube-dl -x --audio-format=wav --output "' + vid + '.%(ext)s" https://www.youtube.com/watch?v=' + vid + ">NUL")
    elif osis == "Linux" or osis == "Darwin":
        os.system('youtube-dl -x --audio-format=wav --output "./' + vid + '.%(ext)s" https://www.youtube.com/watch?v=' + vid + ">/dev/null")
    else:
        trashbin = ""

def sys_AudioPlayer():
    TitlenoLoop = 0
    global songs_dl
    global np
    global hr_enabled
    while 1 == 1:
        if not songs_dl:
            if TitlenoLoop >= 1:
                pass
            else:
                if osis == "Windows":
                    ctypes.windll.kernel32.SetConsoleTitleW("■ Play anything you want")
                if RPC != None:
                    RPC.update(state="노동요 듣는중", details="예약된 곡 없음")
                TitlenoLoop += 1
        else:
            np = songs_dl[0]
            del songs_dl[0]
            TitlenoLoop = 0
            if osis == "Windows":
                ctypes.windll.kernel32.SetConsoleTitleW("▶ " + np[0])
            if RPC != None:
                RPC.update(state="노동요 듣는중", details=np[0])
            hr_enabled = False
            if hr:
                play_obj = simpleaudio.play_buffer(np[3], np[4], np[5], np[6])
            else:
                wave_obj = simpleaudio.WaveObject.from_wave_file(np[1] + '.wav')
                os.remove(np[1] + '.wav')
                play_obj = wave_obj.play()
            play_obj.wait_done()
            wave_obj = None
            play_obj = None
            np = None
        time.sleep(.5)

def sys_AutoDownloader():
    global songs
    global songs_dl
    global hr
    while 1 == 1:
        if not songs:
            pass
        else:
            if os.path.isfile(songs[0][1] + ".wav"):
                pass
            else:
                sys_DownloadSong(songs[0][1])
            if hr:
                wave_read = wave.open(songs[0][1] + ".wav", 'rb')
                audio_data = wave_read.readframes(wave_read.getnframes())
                num_channels = wave_read.getnchannels()
                bytes_per_sample = wave_read.getsampwidth()
                sample_rate = wave_read.getframerate()
                songs_dl.append([songs[0][0], songs[0][1], songs[0][2], audio_data, num_channels, bytes_per_sample, sample_rate])
                wave_read.close()
                wave_read = None
                audio_data = None
                num_channels = None
                bytes_per_sample = None
                sample_rate = None
                os.remove(songs[0][1] + '.wav')
            else:
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
        print("===== generic commands =====")
        print("h            : this help")
        print("r (keyword)  : search song and add to playlist")
        print("l            : print playlist")
        print("sf           : shuffle playlist")
        print("del (number) : delete item in playlist")
        print("pr (number)  : priorite playlist item to next song")
        print("sk           : skip current song")
        print("np           : show what song is playing now")
        print("=====  player options  =====")
        print("qp           : toggles quick play")
        print("               always play 1st item in search")
        print("hr           : huge RAM consuming mode")
        print("               stores downloaded songs to RAM directly")
        print("               use this command before playing song.")
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
                if not hr:
                    os.remove(songs_dl[n][1] + '.wav')
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
                npr = None
            except:
                print("invalid number")
    elif inp == "sk":
        simpleaudio.stop_all()
    elif inp == "np":
        print("Now playing : " + np[0])
    elif inp == "qp":
        if qp:
            qp = False
            print("quick play disabled")
        else:
            qp = True
            print("quick play enabled")
    elif inp == "hr":
        if hr_enabled:
            if hr:
                hr = False
                print("huge RAM consuming mode disabled")
            else:
                hr = True
                print("huge RAM consuming mode enabled")
        else:
            print("please restart app and use this command before playing song.")
    else:
        continue