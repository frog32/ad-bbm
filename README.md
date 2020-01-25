# bbm - Black Box Monitoring

*bbm is an [AppDaemon](https://github.com/home-assistant/appdaemon) app which measures latency in Home Assistant.*

## Supprted Monitoring Platforms

* Stackdriver Monitoring

## Installation

[Download](https://github.com/frog32/ad-bbm/releases) the `bbm` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `bbm` module.

## App configuration

This is an example configuration that assumes that switch.ping is coupled to binary_sensor.pong (hard wired or using some other means).

```yaml
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
```

### Monitoring Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | prober | The module name of the app.
`class` | False | string | StackdriverMonitoring | The name of the python class.
`project` | False | string | none | Google Cloud project identifier.
`credentials_json` | False | path | none | path to your Google Cloud service account credentials file.

### Prober Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | prober | The module name of the app.
`class` | False | string | Prober | The name of the python class.
`ping` | False | entity | Prober | Entity to enable to start a probing cycle.
`pong` | False | entity | Prober | Entity that responds back.
`metric_name` | False | string | Prober | Metric name used in monitoring.
