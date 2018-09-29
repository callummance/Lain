from bottle import request, Bottle, template, run, install, JSONPlugin
import json
from bson import json_util

from statspage import data_source

app = Bottle(autojson=False)

class JSONDefaultPlugin(JSONPlugin):
    def __init__(self):
        super(JSONDefaultPlugin, self).__init__()
        self.plain_dump = self.json_dumps
        self.json_dumps = lambda body: self.plain_dump(body, default=json_util.default)

@app.route("/api/speedtests.json")
def get_speedtests():
    return data_source.speedtest_data(app.config["mongo"])

@app.route("/api/pingtests.json")
def get_pingchecks():
    return data_source.pingtest_data(app.config["mongo"])

@app.route("/api/gatewaytests.json")
def get_gatewaychecks():
    return data_source.gatewaytest_data(app.config["mongo"])

def start_server(config):
    app.config["mongo"] = config["mongo"]
    serverconf = config["webserver"]
    app.install(JSONDefaultPlugin())
    run(app, host=serverconf["host"], port=serverconf["port"])
