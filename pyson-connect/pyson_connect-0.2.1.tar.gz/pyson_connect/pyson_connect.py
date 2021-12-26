import os
import json
from .errors import Errors
import requests
from requests.auth import HTTPBasicAuth

from PIL import Image


class PysonConnect:
    def __init__(self, ClientID=None, ClientSecret=None):
        if ClientID == None:
            self.ClientID = os.environ["epsonClientID"]

        else:
            self.ClientID = ClientID

        if ClientSecret == None:
            self.ClientSecret = os.environ["epsonClientSecret"]

        else:
            self.ClientSecret = ClientSecret

        self.err = Errors()
        self.baseURI = "https://api.epsonconnect.com"
        self.accessToken = None
        self.subjectID = None
        self.jobID = None
        self.uploadURI = None
        
    
    def authentification(self, username):
        reqURI = f"{self.baseURI}/api/1/printing/oauth2/auth/token?subject=printer"
        headers = {
                "Content-Type":"application/x-www-form-urlencoded"
                }
        data = {
                "grant_type":"password",
                "username":username,
                "password":""
                }

        r = requests.post(url=reqURI, headers=headers, data=data, auth=HTTPBasicAuth(self.ClientID, self.ClientSecret))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.accessToken = rjson["access_token"]
            expiresIn = rjson["expires_in"]
            refreshToken = rjson["refresh_token"]
            self.subjectID = rjson["subject_id"]

            returnData = {
                    "accessToken":self.accessToken,
                    "expiresIn":expiresIn,
                    "refreshToken":refreshToken,
                    "subjectID":self.subjectID
                    }
            return returnData


    def reissueAccessToken(self, refreshToken):
        reqURI = f"{self.baseURI}/api/1/printing/oauth2/auth/token?subject=printer"
        headers = {
                "Content-Type":"application/x-www-form-urlencoded"
                }
        data = {
                "grant_type":"refresh_token",
                "refresh_token":refreshToken
                }
        r = requests.post(url=reqURI, headers=headers, data=data, auth=HTTPBasicAuth(self.ClientID, self.ClientSecret))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.accessToken = rjson["access_token"]
            expiresIn = rjson["expires_in"]
            self.subjectID = rjson["subject_id"]

            returnData = {
                    "accessToken":self.accessToken,
                    "expiresIn":expiresIn,
                    "subjectID":self.subjectID
                    }
            return returnData

        
    def getDevicePrintCapabilities(self, documentType, accessToken=None, subjectID=None):
        if not accessToken:
            accessToken = self.accessToken

        if not subjectID:
            subjectID = self.subjectID

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/capability/{documentType}"
        headers = {
                "Authorization":f"Bearer {accessToken}"
                }
        r = requests.get(url=reqURI, headers=headers)

        rjson = r.json()
        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

        else:
            return rjson


    def printSetting(self, settingData, accessToken=None, subjectID=None):
        if not accessToken:
            accessToken = self.accessToken

        if not subjectID:
            subjectID = self.subjectID

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/jobs"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":f"application/json"
                }
        r = requests.post(url=reqURI, headers=headers, data=json.dumps(settingData))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.jobID = rjson["id"]
            self.uploadURI = rjson["upload_uri"]

            returnData = {
                    "jobID":self.jobID,
                    "uploadURI":self.uploadURI
                    }
            return returnData
            

    def uploadPrintFile(self, filePath, documentType, jobID=None, uploadURI=None):
        lExt = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".tiff", ".TIFF"]
        dlData = None

        if "http" in filePath:
            lfPath = filePath.split(".")
            tmpName = lfPath[-2]
            name = tmpName.split("/")[-1]
            extension = lfPath[-1]
            dlData = f"{name}.{extension}"
            r = requests.get(filePath)
            statusCode = r.status_code
            if statusCode != 200:
                r.raise_for_status()
            
            else:
                data = r.content
                with open(dlData, "wb") as f:
                    f.write(data)

                filePath = dlData

        extension = os.path.splitext(filePath)[1]
        name = os.path.splitext(filePath)[0]
        if str(extension) in lExt:
            exifImg = Image.open(filePath)
            imgData = exifImg.getdata()
            mode = exifImg.mode
            size = exifImg.size

            delExif = Image.new(mode, size)
            delExif.putdata(imgData)
            delExif.save(f"del_{name}{extension}")

            filePath = f"del_{name}{extension}"

        with open(filePath, "rb") as f:
            data = f.read()
            
        dataSize = os.path.getsize(filePath)
        if documentType == "document" and dataSize < 200000000:
            ContentType = "application/octet-stream"
            
        elif documentType == "photo" and dataSize < 100000000:
            ContentType = "image/jpeg"

        else:
            self.err.errors()

        reqURI = f"{self.uploadURI}&File=1{extension}"
        headers = {
                "Content-Length":str(dataSize),
                "Content-Type":ContentType
                }
        r = requests.post(url=reqURI, headers=headers, data=data)
        statusCode = r.status_code
        
        if statusCode != 200:
            self.err.errors(statusCode=statusCode)
        
        else:
            if dlData:
                os.remove(dlData)

            if "del_" in filePath:
                os.remove(filePath)


    def excutePrint(self, accessToken=None, subjectID=None, jobID=None):
        if accessToken == None:
            accessToken = self.accessToken
            
        if subjectID == None:
            subjectID = self.subjectID

        if jobID == None:
            jobID = self.jobID

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/jobs/{jobID}/print"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        r = requests.post(url=reqURI, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def cancelPrint(self, accessToken, subjectID, jobID, opBy="user"):
        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/jobs/{jobID}/cancel"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        data = {
                "operated_by":opBy
                }
        r = requests.post(url=reqURI, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def getPrintJobInfo(self, accessToken=None, subjectID=None, jobID=None):
        if accessToken == None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID

        if jobID == None:
            jobID = self.jobID

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/jobs/{jobID}"
        headers = {
                "Authorization":f"Bearer {accessToken}"
                }
        r = requests.get(url=reqURI, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

        else:            
            status = rjson["status"]
            statusReason = rjson["status_reason"]
            startDate = rjson["start_date"]
            jobName = rjson["job_name"]
            ttlPages = rjson["total_pages"]
            updateDate = rjson["update_date"]

            returnData = {
                    "status":status,
                    "statusReason":statusReason,
                    "startDate":startDate,
                    "jobName":jobName,
                    "ttlPages":ttlPages,
                    "updateDate":updateDate
                    }
            return returnData


    def getDeviceInfo(self, accessToken=None, subjectID=None):
        if accessToken == None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}"
        headers = {
                "Authorization":f"Bearer {accessToken}"
                }
        r = requests.get(url=reqURI, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            printerName = rjson["printer_name"]
            serialNo = rjson["serial_no"]
            ecConnected = rjson["ec_connected"]

            returnData = {
                    "printerName":printerName,
                    "serialNo":serialNo,
                    "ecConnected":ecConnected
                    }
            return returnData


    def cancelAuthentication(self, accessToken, subjectID):
        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}"
        headers = {
                "Authorization":f"Bearer {accessToken}" 
                }
        r = requests.delete(url=reqURI, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def notificationSetting(self, data, accessToken=None, subjectID=None):
        if accessToken==None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID 

        reqURI = f"{self.baseURI}/api/1/printing/printers/{subjectID}/settings/notification"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        r = requests.post(url=reqURI, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def getScanDestinationList(self, accessToken=None, subjectID=None):
        if accessToken==None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID 

        reqURI = f"{self.baseURI}/api/1/scanning/scanners/{subjectID}/destinations"
        headers = {
                "Authorization":f"Bearer {accessToken}"
                }
        r = requests.get(url=reqURI, headers=headers)
        rjson = r.json()

        dests = []
        destData = {}
        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            destinations = rjson["destinations"]
            for dest in destinations:
                destData["scanDestID"] = dest["id"]
                destData["AliasName"] = dest["alias_name"]
                destData["destType"] = dest["type"]
                destData["destination"] = dest["destination"]
                dests.append(destData)
                destData = {}

            returnData = {
                    "destinations":dests
                    }
            return returnData


    def registerScanDestination(self, data, accessToken=None, subjectID=None):
        if accessToken == None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID

        reqURI = f"{self.baseURI}/api/1/scanning/scanners/{subjectID}/destinations"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        data = {
                "alias_name":data["AliasName"],
                "type":data["destType"],
                "destination":data["destination"]
                }
        r = requests.post(url=reqURI, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def updateScanDestination(self, data, accessToken=None, subjectID=None):
        if accessToken == None:
            accessToken = self.accessToken

        if subjectID == None:
            subjectID = self.subjectID

        reqURI = f"{self.baseURI}/api/1/scanning/scanners/{subjectID}/destinations"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        data = {
                "id":data["scanDestID"],
                "alias_name":data["AliasName"],
                "type":data["destType"],
                "destination":data["destination"]
                }
        r = requests.put(url=reqURI, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

    
    def deleteScanDestination(self, accessToken, subjectID, scanDestID):
        reqURI = f"{self.baseURI}/api/1/scanning/scanners/{subjectID}/destinations"
        headers = {
                "Authorization":f"Bearer {accessToken}",
                "Content-Type":"application/json"
                }
        data = {
                "id":scanDestID
                }
        r = requests.delete(url=reqURI, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
