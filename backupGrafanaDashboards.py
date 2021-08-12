import requests, json
import os, subprocess, shutil, time, sys
from datetime import datetime
sys.path.append(".")

class GrafanaDashboardBackups():
    grafanaBaseUrl = "http://172.10.10.100:3000"
    access_token = "write your access token here"
    my_headers = {'Authorization' : "Bearer " + access_token}
    apiSearchUrl = "/api/search?query=%"
    apiDashboardUrl = "/api/dashboards/uid/"

    dirDate = datetime.now().strftime("%d%m%y")
    dirDatePretty = datetime.now().strftime("%d-%m-%y %H:%m")
    dirName = "Grafana-Backup"
    path = '.'
    foundCreatedDate = []
    foundFolderNames = []
    uidArr = []
    title = []

    keepLastBackupCount = 5

    def getUrl(self):
        counter = 0
        try:
            #search all dashboards and find uids
            response = requests.get(self.grafanaBaseUrl + self.apiSearchUrl,headers=self.my_headers)
            for idx,resp in enumerate(response.json()):
                self.uidArr.append(resp["uid"])
                self.title.append(resp["title"])
                counter = idx+1

            #create backup folder
            scriptPath = os.path.join(self.path, self.dirName + "-" + self.dirDate)
            # run if dashboard file does not exists
            if not os.path.exists(scriptPath):
                os.makedirs(scriptPath)
                for idx,uid in enumerate(self.uidArr):
                    #search all dashboards meta and write them into a file as json
                    response = requests.get(self.grafanaBaseUrl + self.apiDashboardUrl + uid, headers=self.my_headers)
                    prettyFileName = ''.join(e for e in self.title[idx] if e.isalnum())
                    print("{} - writing \"{}\" file".format((idx + 1), prettyFileName))
                    with open(os.path.join(scriptPath,prettyFileName+".json"),'w') as f:
                        json.dump(response.json()["dashboard"],f)

            print("**********************************")
            print("{} dashboards has been found!".format(counter))
        except requests.exceptions.HTTPError as httpErr:
            print("http error:",httpErr)
            return True, -1
        except requests.exceptions.ConnectionError as connectErr:
            print("connection error:",connectErr)
            return True, -1
        except requests.exceptions.Timeout as timeErr:
            print("timeout error:",timeErr)
            return True, -1
        except requests.exceptions.RequestException as reqErr:
            print("request error:",reqErr)
            return True, -1
        return False, counter

    def getFolderNamesAndCreatedDates(self):
        counter = 0
        print("************* BEGIN {} *************".format(self.dirDatePretty))
        # find backup folder names in {path} path
        backupFolderNames = [name for name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, name))]

        for idx,folder in enumerate(backupFolderNames):
            if self.dirName.lower() in folder.lower():
                folderPath = os.path.join(self.path, folder)
                creDate = datetime.strptime(time.ctime(os.path.getctime(folderPath)), "%a %b %d %H:%M:%S %Y")
                print("{}- name: {}, created date: {}".format(counter+1,folder,creDate))
                x =  "{}{}{}{}{}{}".format(creDate.year,creDate.month,creDate.day,creDate.hour,creDate.minute,creDate.second)
                #print("x:{}".format(x))
                self.foundCreatedDate.append(x)
                self.foundFolderNames.append(folder)
                counter += 1

        print("**********************************")
        print("{} backup folders has been found!".format(counter))
        return counter

    def sortLists(self):
        # sort date array to find old backups
        for iter_num in range(len(self.foundCreatedDate)-1,0,-1):
            for idx in range(iter_num):
                if self.foundCreatedDate[idx]<self.foundCreatedDate[idx+1]:
                    temp = self.foundCreatedDate[idx]
                    self.foundCreatedDate[idx] = self.foundCreatedDate[idx+1]
                    self.foundCreatedDate[idx+1] = temp

                    temp = self.foundFolderNames[idx]
                    self.foundFolderNames[idx] = self.foundFolderNames[idx+1]
                    self.foundFolderNames[idx+1] = temp

    def deleteFolders(self,counter):
        print("************* RESULT *************")
        print("PS: Keeping last \"{}\" backups on the server!".format(self.keepLastBackupCount))
        if counter > self.keepLastBackupCount:
            for folder in self.foundFolderNames[self.keepLastBackupCount:]:
                print("deleting \"{}\" folder".format(folder))
                folderPath = os.path.join(self.path, folder)
                shutil.rmtree(folderPath)
        else:
            print("No folder will be deleting at this time!")

if __name__ == '__main__':
    grafana = GrafanaDashboardBackups()
    ifErr, dashboard_count = grafana.getUrl()
    if not ifErr:
        counter = grafana.getFolderNamesAndCreatedDates()
        grafana.sortLists()
        grafana.deleteFolders(counter)