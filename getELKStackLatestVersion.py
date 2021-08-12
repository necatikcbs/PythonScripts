import re, os, requests
from bs4 import BeautifulSoup

class FindVersionsOfTools:
    def __init__(self):
        self.elasticDownloadUrl = "https://www.elastic.co/downloads"
        self.grafanaDownloadUrl = "https://grafana.com/grafana/download?utm_source=grafana_footer"
        self.toolNames = ["grafana", "elasticsearch", "kibana", "logstash"]
        self.elkNames = ["elasticsearch", "kibana", "logstash"]
        self.path = os.path.dirname(__file__)

    def getELKVersions(self):
        print("********** Getting ELK Latest Versions **********")
        try:
            for name in self.elkNames:
                html_text = requests.get("{}/{}".format(self.elasticDownloadUrl, name)).text
                soup = BeautifulSoup(html_text, 'html.parser')
                attributes = soup.find("div", {"class": "react-tabs__tab-panel"})

                textDivRegex = re.compile("jsx-.* col-4 text-right", re.I)
                versionDivRegex = re.compile("jsx-.* col-8", re.I)
                for attr in attributes.find_all("div", attrs={"class": textDivRegex}):
                    if attr.text == "Version:":
                        latestVersion = (attributes.find("div", attrs={"class": versionDivRegex})).text

                print("{} version: {}".format(name.capitalize(), latestVersion))
        except Exception as e:
            print("getELKVersions:Some error occured!")
            print(e)

if __name__ == '__main__':
    tool = FindVersionsOfTools()
    tool.getELKVersions()