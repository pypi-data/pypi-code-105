import requests

def notify(to, subject="", text=""):
    """ Send notification from python scripts to FatBeagle notification system """
    assert type(to) == type([])
    assert len(to) > 0
    mailObject = {}
    mailObject['subject'] = subject
    mailObject['text'] = text
    mailObject['to'] = ', '.join(to)

    x = requests.post("http://localhost:3000/send-noti", json = mailObject)

    if x.status_code == 200:
        print("Notification sent")
    else:
        print("Notification failed")
        
    print(x.text)