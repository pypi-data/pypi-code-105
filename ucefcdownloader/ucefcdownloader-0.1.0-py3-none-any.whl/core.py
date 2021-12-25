from .utils import ThreadWrapper
import traceback
import threading
import requests
import zipfile
import shutil
import json
import os
import re
import io


class UCEFCDownloader:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"user-agent": "Chrome/96.1.23.63221"})

    @staticmethod
    def check_zipfile(fo):
        zip_fo = zipfile.ZipFile(fo, "r")
        compilation = []
        for i, name in enumerate(zip_fo.namelist()):
            if not name.endswith(".txt"):
                raise
            if name == "how_to_download.txt":
                continue
            print("\r", i+1, len(zip_fo.namelist()), name, end="", flush=True)
            link = zip_fo.read(name).decode()
            if not re.search(r"^https?://ucefc(\.[a-z0-9]+)+/[A-Za-z0-9]+$", link):
                raise
            compilation.append([name, link])
        zip_fo.close()
        print(flush=True)
        return compilation

    def get_download_link(self, link):
        domain = "/".join(link.split("/")[:3])
        r = self.s.post(domain+"/api", {"op": "clone_file", "id": link.split("/")[-1]})
        if r.status_code == 200:
            url = r.json()
            url = domain.replace("ucefc.", "resolve.ucefc.")+"/"+url.split("/")[-1]
            r = self.s.get(url)
            if r.status_code == 200:
                return r.content.decode()
            else:
                raise Exception([r.status_code, r.content.decode()])
        else:
            raise Exception([r.status_code, r.content.decode()])

    def dl_zipfile(self, link):
        fo = io.BytesIO()
        print("resolving link", link, flush=True)
        link = self.get_download_link(link)
        print("downloading zip file", link, flush=True)
        r = self.s.get(link)
        if r.status_code == 200:
            fo.write(r.content)
        else:
            raise Exception([r.status_code, r.content.decode()])
        fo.seek(0)
        return self.check_zipfile(fo)

    def gen_queue(self, what):
        if os.path.isfile("queue.json"):
            print("skipping, queue.json exists", flush=True)
            return
        compilation = self.dl_zipfile(what)
        queue = {}
        tw = ThreadWrapper(threading.Semaphore(2**2))
        for i, (fp, link) in enumerate(compilation):
            def job(i, fp, link):
                def _job():
                    print("\r", i+1, len(compilation), fp, link, end="", flush=True)
                    return [fp, self.get_download_link(link)]
                return _job
            tw.add(job=job(i, fp[:-4], link), result=queue, key=i)
        tw.wait()
        print(flush=True)
        print(os.getcwd(), queue, flush=True)
        open("queue.json", "wb").write(json.dumps(queue).encode())

    def download(self, cb=None):
        queue = json.loads(open("queue.json", "rb").read().decode())
        queue = dict(sorted(queue.items(), key=lambda x: int(x[0])))
        _l = len(queue)
        for i, (fp, link) in list(queue.items()):
            try:
                r = callable(cb) and cb(int(i)+1, _l, fp, link)
                if r is not False:
                    queue.pop(i)
                open("queue.json", "wb").write(json.dumps(queue).encode())
            except:
                traceback.print_exc()
        if not queue:
            os.remove("queue.json")
        else:
            shutil.move("queue.json", "skipped.json")


