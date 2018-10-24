import unittest
from .parser import Parser
from influx_line_protocol import Metric
from influx_line_protocol import MetricCollection


class ParserTest(unittest.TestCase):
    stats_data = {
        "pods": [
            {
                "podRef": {
                    "name": "canal-fqwlv",
                    "namespace": "kube-system",
                    "uid": "073e8d80-d205-11e8-aa15-0a8d2358674a"
                },
                "startTime": "2018-10-17T12:06:07Z",
                "containers": [
                    {
                        "name": "install-cni",
                        "startTime": "2018-10-17T12:06:08Z",
                        "cpu": {
                            "time": "2018-10-18T10:16:10Z",
                            "usageNanoCores": 44756,
                            "usageCoreNanoSeconds": 4100063774
                        },
                        "memory": {
                            "time": "2018-10-18T10:16:10Z",
                            "usageBytes": 73990144,
                            "workingSetBytes": 30420992,
                            "rssBytes": 180224,
                            "pageFaults": 428434,
                            "majorPageFaults": 0
                        },
                        "rootfs": {
                            "time": "2018-10-18T10:16:10Z",
                            "availableBytes": 44108034048,
                            "capacityBytes": 51976970240,
                            "usedBytes": 49152,
                            "inodesFree": 6258060,
                            "inodes": 6400000,
                            "inodesUsed": 13
                        },
                        "logs": {
                            "time": "2018-10-18T10:16:10Z",
                            "availableBytes": 44108034048,
                            "capacityBytes": 51976970240,
                            "usedBytes": 20480,
                            "inodesFree": 6258060,
                            "inodes": 6400000,
                            "inodesUsed": 141940
                        },
                    }
                ],
                "cpu": {
                    "time": "2018-10-18T10:16:10Z",
                    "usageNanoCores": 11042312,
                    "usageCoreNanoSeconds": 976808301996
                },
                "memory": {
                    "time": "2018-10-18T10:16:10Z",
                    "usageBytes": 106688512,
                    "workingSetBytes": 63107072,
                    "rssBytes": 28389376,
                    "pageFaults": 0,
                    "majorPageFaults": 0
                },
                "network": {
                    "time": "2018-10-18T10:16:03Z",
                    "name": "",
                    "interfaces": [
                        {
                            "name": "cali3e3082340d7",
                            "rxBytes": 227051613,
                            "rxErrors": 0,
                            "txBytes": 181652981,
                            "txErrors": 0
                        }
                    ]
                },
                "volume": [
                    {
                        "time": "2018-10-17T12:06:49Z",
                        "availableBytes": 4030717952,
                        "capacityBytes": 4030730240,
                        "usedBytes": 12288,
                        "inodesFree": 984056,
                        "inodes": 984065,
                        "inodesUsed": 9,
                        "name": "canal-token-9hlfs"
                    }
                ],
                "ephemeral-storage": {
                    "time": "2018-10-18T10:16:10Z",
                    "availableBytes": 44108034048,
                    "capacityBytes": 51976970240,
                    "usedBytes": 229376,
                    "inodesFree": 6258060,
                    "inodes": 6400000,
                    "inodesUsed": 46
                }
            }
        ]
    }

    def setUp(self):
        self.expectedCollection = MetricCollection()
        m = Metric("kubernetes_pod")
        m.add_tag("pod", "canal-fqwlv")
        m.values = {
            'cpu_usage': '0.0110423',
            'memory_rssBytes': '28389376',
            'memory_usageBytes': '106688512',
            'memory_workingSetBytes': '63107072',
            'memory_pageFaults': '0',
            'memory_majorPageFaults': '0'
        }
        self.expectedCollection.append(m)
        m = Metric("kubernetes_pod_network")
        m.add_tag("pod", "canal-fqwlv")
        m.add_tag("interface", "cali3e3082340d7")
        m.values = {
            'rxBytes': '227051613',
            'rxErrors': '0',
            'txBytes': '181652981',
            'txErrors': '0'
        }
        self.expectedCollection.append(m)
        m = Metric("kubernetes_pod_container")
        m.add_tag("pod", "canal-fqwlv")
        m.add_tag("container", "install-cni")
        m.values = {
            'cpu_usage': '4.4756e-05',
            'memory_rssBytes': '180224',
            'memory_usageBytes': '73990144',
            'memory_workingSetBytes': '30420992',
            'memory_pageFaults': '428434',
            'memory_majorPageFaults': '0'
        }
        self.expectedCollection.append(m)

    def test_pod_metrics(self):
        stats_data = self.stats_data

        a = Parser()
        collection = a.parse_stats(stats_data)

        self.maxDiff = None
        self.assertDictEqual(
            self.expectedCollection.metrics[0].values,
            collection.metrics[0].values)

    def test_pod_containersmetrics(self):
        stats_data = self.stats_data

        a = Parser()
        collection = a.parse_stats(stats_data)

        self.maxDiff = None
        self.assertDictEqual(
            self.expectedCollection.metrics[1].values,
            collection.metrics[1].values)
