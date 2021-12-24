import os
import sys
from colorama import Fore as f
from time import sleep
import datetime
import pytube
from pytube import YouTube as y
from better_ffmpeg_progress import FfmpegProcess as ffmpeg
import validators

args = []


def Close(Code=None):
    if (len(args) != 0):
        if (args[0] == "-i" or args[0] == "-help") == False:
            print("Deleting temp files...")
    sleep(1)
    for i in ["logs.tmp", "video.tmp", "audio.tmp"]:
        if (os.path.exists(i)):
            os.remove(i)
    if Code == None:
        sys.exit()
    else:
        ShowHelp()
        sys.exit(f"{f.RED}{Code}{f.WHITE}")


def AskToOverwrite(data):
    if (data == "-a") and (os.path.exists(vid.name_formatted + ".mp3")):
        while True:
            option = input(
                f"{f.BLUE}File '{vid.name_formatted}.mp3' already exists. Overwrite ? [Y/n] {f.WHITE}").lower()
            if option == "y" or option == "":
                break
            elif option == "n":
                print("Stopping...")
                sleep(1.5)
                Close()
            else:
                print("Not an option")
    if (data != "-a") and (os.path.exists(vid.name_formatted + ".mp4")):
        while True:
            option = input(
                f"{f.BLUE}File '{vid.name_formatted}.mp4' already exists. Overwrite ? [Y/n] {f.WHITE}").lower()
            if option == "y" or option == "":
                break
            elif option == "n":
                print("Stopping...")
                sleep(1.5)
                Close()
            else:
                print("Not an option")


def ShowHelp():
    print(
        '''\nInput: [Program name] [Option] [Link] [Search term] [Video type] [-o]

Options: -d, -i, -s, -help
    -d: Download
    -i: Show info
    -s: Search youtube and download first video
    -help: Show this menu

Search term:
    If using "-s" then enter your search term here, if not using "-s" then ignore this

Video type: 144p, 240p, etc or -a for audio
-o: Adding -o opens the file when done

Examples: 
    If you wanted to download a video at 720p: tube -d <link> 720p
    If you wanted to download a video and open it after downloaded: tube -d <link> <resolution> -o
    If you wanted to download audio of a video: tube -d <link> -a
    If you wanted to show info about a video: tube -i <link>
    If you wanted to download a video that has something to do with apples: tube -s apples
\n''')


class SearchYoutube():
    def __init__(self, SearchTerm):
        from pytube import Search
        s = Search(SearchTerm)
        self.amount = len(s.results)
        self.results = s.results
        self.search = s

    def GetMore(self):
        self.search.get_next_results()


class GetVideo():
    def __init__(self, link=None, vid=None):
        if link != None:
            print("Getting video...")
            if (bool(validators.url(link))) == False:
                Close(f"Invalid link")
            self.yt = y(link)
        else:
            self.yt = vid
        print("Checking video...")
        try:
            self.yt.title
        except pytube.exceptions.VideoPrivate:
            Close(f"Video is private")
        self.name_formatted = self.yt.title
        for i in ["/", "\\", ":", "*", "?", '"', ">", "<", "|"]:
            self.name_formatted = self.name_formatted.replace(i, "_")
        self.audios = self.yt.streams.filter(
            only_audio=True, file_extension="webm")
        self.videos = self.yt.streams.filter(
            file_extension="mp4", adaptive=True, only_video=True)
        self.resolutions = []
        for i in ["144p", "240p", "360p", "480p", "720p", "1080p"]:
            if (len(self.videos.filter(res=i)) > 0):
                self.resolutions.append(i)

    def GetFormattedInfo(self):
        date = self.yt.publish_date
        return f'''\nAvailable resolutions: {", ".join(self.resolutions)}
Video title: {self.yt.title}
Video author: {self.yt.author}
Video length: {datetime.timedelta(seconds=int(self.yt.length))}
Upload date: {"/".join([str(date.month), str(date.day), str(date.year)])}
Views: {self.yt.views}'''

    def DownloadVideo(self, res):
        FilesizeB = self.videos.filter(res=res).first(
        ).filesize + self.audios.last().filesize
        size = ""
        if FilesizeB > 1073741824:
            size = str(round(FilesizeB / 1024 / 1024 / 1024, 2)) + "GB"
        else:
            if FilesizeB > 1048576:
                size = str(round(FilesizeB / 1024 / 1024, 2)) + "MB"
            else:
                if FilesizeB > 1024:
                    size = str(round(FilesizeB / 1024), 2) + "KB"
                else:
                    size = str(round(FilesizeB), 2) + "B"
        while True:
            option = input(
                f"{f.BLUE}This will take up about {size}. Continue ? [Y/n] {f.WHITE}").lower()
            if option == "y" or option == "":
                break
            elif option == "n":
                print("Stopping...")
                sleep(1.5)
                Close()
            else:
                print("Not an option")

        print("Downloading video...")
        sleep(1)
        try:
            self.videos.filter(res=res).first().download(filename="video.tmp")
            print("Downloading audio...")
            sleep(1)
            self.audios.last().download(filename="audio.tmp")
            print("Done downloading")
            sleep(1)
        except Exception:
            Close("Error in downloading files")
        print("Combining audio with video...")
        process = ffmpeg(["ffmpeg", "-y", "-i", "video.tmp",
                         "-i", "audio.tmp", "video.mp4"])
        process.run(ffmpeg_output_file="logs.tmp")
        if (os.path.exists(self.name_formatted + ".mp4")):
            os.remove(self.name_formatted + ".mp4")
        os.rename("video.mp4", self.name_formatted + ".mp4")

    def DownloadAudio(self):

        FilesizeB = self.audios.last().filesize
        size = ""
        if FilesizeB > 1073741824:
            size = str(round(FilesizeB / 1024 / 1024 / 1024, 2)) + "GB"
        else:
            if FilesizeB > 1048576:
                size = str(round(FilesizeB / 1024 / 1024, 2)) + "MB"
            else:
                if FilesizeB > 1024:
                    size = str(round(FilesizeB / 1024), 2) + "KB"
                else:
                    size = str(round(FilesizeB), 2) + "B"
        while True:
            option = input(
                f"{f.BLUE}This will take up about {size}. Continue ? [Y/n] {f.WHITE}").lower()
            if option == "y" or option == "":
                break
            elif option == "n":
                print("Stopping...")
                sleep(1.5)
                Close()
            else:
                print("Not an option")

        print("Downloading audio...")
        sleep(1)
        try:
            self.audios.last().download(filename="audio.tmp")
            print("Done downloading")
            sleep(1)
        except Exception:
            Close("Error in downloading files")
        print("Converting file...")
        process = ffmpeg(["ffmpeg", "-y", "-i", "audio.tmp", "audio.mp3"])
        process.run(ffmpeg_output_file="logs.tmp")
        if (os.path.exists(self.name_formatted + ".mp3")):
            os.remove(self.name_formatted + ".mp3")
        os.rename("audio.mp3", self.name_formatted + ".mp3")
        print(f"{f.GREEN}Finished{f.WHITE}")


def Main(argsv):
    global args
    args = argsv
    global vid

    # Checking command is correctly formatted
    if len(args) == 0:
        Close(f"Syntax error")
    if (args[0] in ["-d", "-i", "-help", "-s"]) == False:
        Close(f"Syntax error")

    if args[0] == "-help":
        ShowHelp()

        Close()

    if (len(args) == 1):
        Close(f"Syntax error")

    print("Checking if ffmpeg is installed...")
    sleep(1)
    code = os.system("ffmpeg -version > ffmpeg.tmp 2>&1")
    os.remove("ffmpeg.tmp")

    if (code != 0):
        Close("FFmpeg not installed or there was a error trying to open it")
    if (args[0] == "-s"):
        print("Getting most relevant video...")
        sleep(1)
        search = SearchYoutube(args[1])
        vid = GetVideo(vid=search.results[0])
        print("Most relevant video: ")
        print(vid.GetFormattedInfo())
        while True:
            option = input("Do you want to download this ? [Y/n] ").lower()
            if (option == "y" or option == ""):
                break
            elif (option == "n"):
                print("Stopping...")
                sleep(1.5)
                Close()
            else:
                print("Not an option")

        while True:
            option = input(
                "What video type do you want ? [<resolution>p, -a] ").lower()
            if (option in vid.resolutions or option == "-a") == False:
                print("Invalid video type")
            else:
                break

        if (option == "-a"):
            vid.DownloadAudio()
        else:
            vid.DownloadVideo(option)
        Close()

    vid = GetVideo(link=args[1])
    if args[0] != "-i":
        if len(args) > 2:
            if (args[2] in vid.resolutions or args[2] == "-a") == False:
                Close("Invalid video type")
        else:
            Close("Syntax error")
        if len(args) > 3:
            if args[3] != "-o":
                Close("Syntax error")

    if args[0] == "-i":
        print(vid.GetFormattedInfo())
        Close()

    AskToOverwrite(args[2])

    if args[2] == "-a":
        vid.DownloadAudio()
        if len(args) > 3:
            if args[3] == "-o":
                print("Opening file...")
                sleep(1)
                os.startfile(vid.name_formatted + ".mp3")
        Close()

    vid.DownloadVideo(args[2])
    if len(args) > 3:
        if args[3] == "-o":
            print("Opening file...")
            sleep(1)
            os.startfile(vid.name_formatted + ".mp4")
    Close()
