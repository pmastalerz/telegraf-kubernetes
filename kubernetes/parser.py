from influx_line_protocol import Metric, MetricCollection


class Parser(object):

    def parse_stats(self, stats):
        collections = MetricCollection()

        for pod in stats["pods"]:
            m = Metric("kubernetes_pod")
            m.add_tag("pod", pod["podRef"]["name"])
            m.add_value("cpu_usage", pod["cpu"]["usageNanoCores"] / 1000000000)
            if "availableBytes" in pod["memory"]:
                m.add_value(
                    "memory_available",
                    pod["memory"]["availableBytes"])
            if "usageBytes" in pod["memory"]:
                m.add_value("memory_usage", pod["memory"]["usageBytes"])
            if "workingSetBytes" in pod["memory"]:
                m.add_value(
                    "memory_working_set",
                    pod["memory"]["workingSetBytes"])
            if "rssBytes" in pod["memory"]:
                m.add_value("memory_rss", pod["memory"]["rssBytes"])
            collections.append(m)
            for container in pod["containers"]:
                m = Metric("kubernetes_pod_container")
                m.add_tag("pod", pod["podRef"]["name"])
                m.add_tag("container", container["name"])
                m.add_value(
                    "cpu_usage",
                    container["cpu"]["usageNanoCores"] /
                    1000000000)
                if "availableBytes" in container["memory"]:
                    m.add_value(
                        "memory_available",
                        container["memory"]["availableBytes"])
                if "usageBytes" in container["memory"]:
                    m.add_value(
                        "memory_usage",
                        container["memory"]["usageBytes"])
                if "workingSetBytes" in container["memory"]:
                    m.add_value(
                        "memory_working_set",
                        container["memory"]["workingSetBytes"])
                if "rssBytes" in container["memory"]:
                    m.add_value("memory_rss", container["memory"]["rssBytes"])
                collections.append(m)

        return collections
