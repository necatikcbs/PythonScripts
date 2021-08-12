import re, os, requests
from requests.auth import HTTPBasicAuth

class FindVersionsOfTools:
    def __init__(self):
        self.elasticDownloadUrl = "https://www.elastic.co/downloads"
        self.grafanaDownloadUrl = "https://grafana.com/grafana/download?utm_source=grafana_footer"
        self.toolNames = ["grafana", "elasticsearch", "kibana", "logstash"]
        self.elkNames = ["elasticsearch", "kibana", "logstash"]
        self.path = os.path.dirname(__file__)

        self.allRegions = []
        self.currentVersionDict = {}
        self.currentVersionDictRegion = {}
        self.currentVersionDictTool = {}

        # this is elasticsearc user. you can add this user via kibana UI
        # this user needs only "monitor" role under the "Cluster privileges". that'll be enough
        # ex. http://172.10.10.106:5601/app/kibana#/management/security/users
        self.toolUser = "apiUser"
        self.toolPasswd = "topSecretPassword"
        self.toolUrls = {
            "grafana": "http://172.10.10.10:3000/api/health",
            "elk": {
                "REGION VENUS": {
                    "kibana": "http://172.10.10.100:5601/api/status",
                    "elasticsearch": {
                        "node1": "http://172.10.10.101:9200/",
                        "node2": "http://172.10.10.102:9200/",
                        "node3": "http://172.10.10.103:9200/"
                    },
                    "logstash": {
                        "node1": "http://172.10.10.104:9600/",
                        "node2": "http://172.10.10.105:9600/"
                    }
                },
                "REGION JUPITER": {
                    "kibana": "http://172.10.10.106:5601/api/status",
                    "elasticsearch": {
                        "node1": "http://172.10.10.107:9200/",
                        "node2": "http://172.10.10.108:9200/",
                        "node3": "http://172.10.10.109:9200/"
                    },
                    "logstash": {
                        "node1": "http://172.10.10.110:9600/",
                        "node2": "http://172.10.10.111:9600/"
                    }
                },
                "REGION NEPTUNE": {
                    "kibana": "http://172.10.10.112:5601/api/status",
                    "elasticsearch": {
                        "node1": "http://172.10.10.113:9200/",
                        "node2": "http://172.10.10.114:9200/",
                        "node3": "http://172.10.10.115:9200/"
                    },
                    "logstash": {
                        "node1": "http://172.10.10.116:9600/",
                        "node2": "http://172.10.10.117:9600/"
                    }
                }
            }
        }

    def getCurrentVersions(self):
        print("********** Getting Current Versions **********")
        try:
            response = requests.get(self.toolUrls["grafana"])
            version = response.json()["version"]
            self.currentVersionDict["grafana"] = version
            print("tool:{}, name:{}, version:{}".format("grafana", "grafana-central", version))
            
            for region in self.toolUrls["elk"]:
                print("********** {} **********".format(region))
                self.allRegions.append(region)
                self.currentVersionDictTool = {}
                for tool in self.toolUrls["elk"][region]:
                    tempDict = {}
                    counter = 0
                    # if tool has no nested value
                    if (not(type(self.toolUrls["elk"][region][tool]) is dict)):
                        response = requests.get(self.toolUrls["elk"][region][tool], auth=HTTPBasicAuth(self.toolUser, self.toolPasswd))
                        version = response.json()["version"]["number"]
                        name = response.json()["name"]
                        tempDict["{}{}".format(name,counter)] = version
                        print("tool:{}, name:{}, version:{}".format(tool, name, version))
                    else:
                        for node in self.toolUrls["elk"][region][tool]:
                            node = node
                            url = self.toolUrls["elk"][region][tool][node]
                            response = requests.get(url, auth=HTTPBasicAuth(self.toolUser, self.toolPasswd))
                            if tool == "logstash":
                                version = response.json()["version"]
                            else:
                                version = response.json()["version"]["number"]
                            name = response.json()["name"]
                            # add counter inside key because of duplicate key problem
                            tempDict["{}{}".format(name,counter)] = version
                            counter += 1
                            print("tool:{}, name:{}, version:{}".format(tool, name, version))
                    self.currentVersionDictTool[tool] = tempDict
                self.currentVersionDictRegion[region] = self.currentVersionDictTool
            self.currentVersionDict["elk"] = self.currentVersionDictRegion
        except Exception as e:
            print("getCurrentVersions:Some error occured!")
            print(e)

if __name__ == '__main__':
    tool = FindVersionsOfTools()
    tool.getCurrentVersions()