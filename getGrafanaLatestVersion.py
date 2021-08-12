import re, os, requests
from bs4 import BeautifulSoup

class FindVersionsOfTools:
    def __init__(self):
        self.elasticDownloadUrl = "https://www.elastic.co/downloads"
        self.grafanaDownloadUrl = "https://grafana.com/grafana/download?utm_source=grafana_footer"
        self.toolNames = ["grafana", "elasticsearch", "kibana", "logstash"]
        self.elkNames = ["elasticsearch", "kibana", "logstash"]
        self.path = os.path.dirname(__file__)

    def getGrafanaVersion(self,url,tag,attribute,attributeValue,list):
        print("********** Getting Grafana Latest Versions **********")
        try:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            selectOptions = soup.find(tag,{attribute: attributeValue})

            for option in selectOptions.find_all(list, selected=True):
                grafanaVersion = option.text
                #print('value: {}, text: {}'.format(option['value'], option.text))

            print("Grafana version: {}".format(grafanaVersion))
        except Exception as e:
            print("getGrafanaVersion:Some error occured!")
            print(e)

if __name__ == '__main__':
    tool = FindVersionsOfTools()
    tool.getGrafanaVersion(tool.grafanaDownloadUrl, "div", "class","download-info-table__row_value", "option")