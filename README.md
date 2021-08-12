# [Backup Grafana Dashboard Script](https://github.com/necatikcbs/PythonScripts/blob/main/backupGrafanaDashboards.py)

This script reaches the Grafana api and creates dashboard files as json in local path in a folder. It also checks the folder counts and deletes if it's bigger then our defined variable, "**keepLastBackupCount**"

You need to define Grafana Url and it's access_token.
```python
grafanaBaseUrl = "http://172.10.10.100:3000"
access_token = "write your access token here"
```

Remember! there is a variable to set "last backup count". You can change it.
```python
keepLastBackupCount = 5
```

# [Get Internal ELK Stack & Grafana Versions](https://github.com/necatikcbs/PythonScripts/blob/main/getCurrentGrafanaElkStackVersions.py)

This script fetches the tool urls that you define as **self.toolUrls** to get versions of these tools in each Region.

```python
self.toolUrls = {
	"grafana": "http://172.10.10.10:3000/api/health",
	"elk": {
		"REGION VENUS": {
			"kibana": "http://172.10.10.100:5601/api/status",
			"elasticsearch": {
				"node1": "http://172.10.10.101:9200/"
			},
			"logstash": {
				"node1": "http://172.10.10.104:9600/",
				"node2": "http://172.10.10.105:9600/"
			}
		},
	.
	.
	.
```

You need to set below parameters. This is elasticsearc user. You can add this user **via kibana UI** for every Region.
This user needs only "monitor" role under the "Cluster privileges". that'll be enough.

to create a user: http://172.10.10.106:5601/app/kibana#/management/security/users

```python
self.toolUser = "apiUser"
self.toolPasswd = "topSecretPassword"
```

# [Get ELK Stack Latest Version](https://github.com/necatikcbs/PythonScripts/blob/main/getELKStackLatestVersion.py)

This script gets ELK Stack(Elasticsearch, logstash, kibana) latest versions from offical elastic website.
This is basically html parse operation.

Just download code and run it!

# [Get Grafana Latest Version](https://github.com/necatikcbs/PythonScripts/blob/main/getGrafanaLatestVersion.py)

This script gets Grafana latest version from offical website. Just download code and run it!