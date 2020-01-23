"""AppDaemon Black Box Prober app.

  @frog32 / https://github.com/frog32/ad-bbm

monitoring:
  module: prober
  class: StackdriverMonitoring
  project: myproject
  credentials_json: "/config/serviceaccount.json"

prober:
  module: prober
  class: Prober
  ping: switch.ping
  pong: binary_sensor.pong
  metric_name: prober_latency
"""

from datetime import datetime, time
from random import randint
from google.cloud import monitoring_v3

import appdaemon.plugins.hass.hassapi as hass

APP_NAME = "BBM"
APP_ICON = "🖥"
APP_VERSION = "0.1"


class StackdriverMonitoring(hass.Hass):
    def initialize(self):
        credentials_json = self.args["credentials_json"]
        self.client = monitoring_v3.MetricServiceClient.from_service_account_json(credentials_json)
        self.project_name = self.client.project_path(self.args["project"])

    def record_value(self, metric_name, value):
        series = monitoring_v3.types.TimeSeries()
        series.metric.type = 'custom.googleapis.com/%s' % metric_name
        series.resource.type = 'global'
        point = series.points.add()
        point.value.double_value = value
        now = time.time()
        point.interval.end_time.seconds = int(now)
        point.interval.end_time.nanos = int(
            (now - point.interval.end_time.seconds) * 10**9)
        self.client.create_time_series(self.project_name, [series])


class Prober(hass.Hass):
    def ping(self, *args):
        self.log("ping")
        self.time = datetime.now()
        self.turn_on(self.ping_entity)

    def pong(self, *args):
        latency = datetime.now() - self.time
        self.log("pong %s" % latency.microseconds)
        monitoring = self.get_app("monitoring")
        monitoring.record_value(self.metric_name, latency.microseconds)

    def initialize(self):
        self.ping_entity = self.args["ping"]
        self.pong_entity = self.args["pong"]
        self.metric_name = self.args["metric_name"]
        self.time = datetime.now()
        self.listen_state(self.pong, self.pong_entity, new="on")
        start_time = time(0, 0, randint(0, 59))
        self.handle = self.run_minutely(self.ping, start_time)
        self.log("Initialized")
