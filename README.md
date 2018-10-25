# telegraf-kubernetes
[![Build Status](https://travis-ci.com/pmastalerz/telegraf-kubernetes.svg?branch=master)](https://travis-ci.com/pmastalerz/telegraf-kubernetes/branches) [![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/pmastalerz/telegraf-kubernetes/blob/master/LICENSE)

Plugin for Telegraf for gathering statistics from Kubernetes

This script is in beta version, use with caution

## Installation
```bash
$ pip install telegraf-kubernetes
```

## Usage
```bash
$ telegraf-kubernetes --stats-url http://10.0.0.222:10255/stats/summary
```

### Optional parameters
* `--timeout` (int)

### Example telegraf configuration
```
[[inputs.exec]]
  commands = ["telegraf-kubernetes --stats-url http://10.0.7.222:10255/stats/summary"]
  data_format = "influx"
```

## License
See [LICENSE](https://github.com/pmastalerz/telegraf-kubernetes/blob/master/LICENSE) file.
