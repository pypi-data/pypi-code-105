import vlc, pafy
import time
import threading
import random

class AudioPlayer:
  def __init__(self, url: str):
    self.mediaResource = pafy.new(url.strip())
    self.player = vlc.MediaPlayer(self.mediaResource.getbestaudio().url)
    self.eventManager = self.player.event_manager()
    self.audioFinished = threading.Condition()
    self.finished = False

    self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached, self.finish)
    self.eventManager.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.finish)

  def play(self):
    self.player.play()
    print('# Now playing: ' + self.mediaResource.title)

  def finish(self, event):
    self.audioFinished.acquire()
    self.finished = True
    self.audioFinished.notifyAll()
    self.audioFinished.release()

  def waitUntilFinished(self):
    self.audioFinished.acquire()
    self.audioFinished.wait_for(lambda: self.finished)
    self.audioFinished.release()

def main():
  with open('playlist.txt', 'r') as playListFile:
    urls = playListFile.readlines()
    while True:
      idx = random.randint(0, len(urls) - 1)
      player = AudioPlayer(urls[idx])
      player.play()
      player.waitUntilFinished()

