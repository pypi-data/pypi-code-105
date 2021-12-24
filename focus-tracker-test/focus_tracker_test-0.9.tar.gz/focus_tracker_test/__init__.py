import argparse
import sys
import win32gui
import uiautomation as auto
import datetime
import easygui
print("Welcome to Focus-Tracker \nYou can list out your distractions and my duty is to save your time by avoiding them")
print("To Start please execute : focus_tracker_test -start START")

def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]

def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        try:
            return 'https://' + edit.GetValuePattern().Value
        except:
            return 'https://'
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return "_active_window_name"

# ctypes.windll.user32.MessageBoxW(0, u"Error", u"BOBO", 0)
def focus_tracker(donot_watch_list):
    print("CTRL+C to Quit:")
    next_time=None
    while True:
        if sys.platform not in ['linux', 'linux2']:
            temp=None
            while True:
                if not temp:
                    temp=""
                window=win32gui.GetForegroundWindow()
                _active_window_name = win32gui.GetWindowText(window)
                if "google chrome" in _active_window_name.lower():
                    chrome_url=get_chrome_url()
                    _active_window_name = url_to_name(chrome_url)
                for i in donot_watch_list:
                    if i.lower() in _active_window_name.lower():
                        present_time=datetime.datetime.now()
                        if not next_time or present_time>next_time:
                            easygui.msgbox("Pss, Please concentrate on your work without deviating", title="Focus-Tracker")
                            next_time=present_time+datetime.timedelta(seconds=3)
                        win32gui.CloseWindow(window)
                        import time;time.sleep(1)

                if _active_window_name!=temp:
                    print(_active_window_name)
                    temp=_active_window_name
        else:
            print("yet to work on this")
            pass

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-start",help="Start Focus Mode")
    args = parser.parse_args()
    if args.start:
        print("Please enter the names of websites/apps which you donot want to open \nPlease press 'q' after you have finished the list")
        donot_watch_list=[]
        while True:
            inp=str(input())
            if "q" in inp:
                break
            donot_watch_list.append(inp)
        focus_tracker(donot_watch_list)

if __name__=='__main__':
    main()


