import os
import requests
import logging

from requests_ntlm import HttpNtlmAuth
from xml.etree import ElementTree


class SharePoint:
    # reference: https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest
    def __init__(self, server, site, user, pwd, debug=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.propagate = debug  # propagate log to higher level

        self.server = server
        self.site = site
        self.user = user
        self.pwd = pwd
        self.auth = HttpNtlmAuth(self.user, self.pwd)

    def list(self, folder):
        url = self.server + '/' + self.site + "/_api/web/GetFolderByServerRelativeUrl('/" + self.site + '/' + folder + "')/Files"
        self.log.debug("url=%s", url)
        files = []
        response = requests.get(url, auth=self.auth)
        tree = ElementTree.fromstring(response.content)
        for entry in tree.iter(tag='{http://www.w3.org/2005/Atom}entry'):
            for content in entry.iter(tag='{http://www.w3.org/2005/Atom}content'):
                for property in content.iter(
                        tag='{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
                    for name in property.iter(tag='{http://schemas.microsoft.com/ado/2007/08/dataservices}Name'):
                        files.append(name.text)
        self.log.debug("files=%s", files)
        return files

    def delete(self, file):
        url = self.server + '/' + self.site + "/_api/web/GetFileByServerRelativeUrl('/" + self.site + '/' + file + "')"
        self.log.debug("url=%s", url)

        # get digest first
        response = requests.post(url, auth=self.auth)
        digest = response.headers['X-RequestDigest']

        headers = {
            'If-Match': "*",
            'X-HTTP-Method': "DELETE",
            'X-RequestDigest': digest,
        }
        response = requests.post(url, auth=self.auth, headers=headers)
        if response.status_code != 200:
            raise Exception("Error response={}".format(response.text))

    def download(self, file, target_file):
        url = self.server + '/' + self.site + '/' + file

        response = requests.get(url, stream=True, auth=self.auth)
        with open(target_file, 'wb') as f:
            f.write(response.content)

    def upload(self, folder, file):
        file_name = os.path.basename(file)

        url = self.server + '/' + self.site + "/_api/web/GetFolderByServerRelativeUrl('/" + self.site + '/' + folder + "')/Files/Add(url='" + file_name + "', overwrite=true)"
        self.log.debug("url=%s", url)

        # get digest first
        response = requests.post(url, auth=self.auth)
        digest = response.headers['X-RequestDigest']

        with open(file, 'rb') as f:
            data = f.read()
            headers = {
                'Content-Length': str(len(data)),
                'X-RequestDigest': digest,
            }
            response = requests.post(url, auth=self.auth, headers=headers, data=data)
            if response.status_code != 200:
                raise Exception("Error response={}".format(response.text))
