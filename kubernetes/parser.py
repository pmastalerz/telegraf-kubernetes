from influx_line_protocol import Metric, MetricCollection


class Parser:

    def __nano_to_deci(self, value):
        return float(value) / 1000000000

    def parse_stats(self, stats):
        collections = MetricCollection()

        for pod in stats["pods"]:
            m = Metric("kubernetes_pod")
            m.add_tag("pod", pod["podRef"]["name"])
            m.add_value(
                "cpu_usage", self.__nano_to_deci(pod["cpu"]["usageNanoCores"]))

            for key, value in pod["memory"].items():
                if key == "time":
                    continue
                m.add_value("memory_%s" % key, value)
            collections.append(m)

            for interface in pod["network"]["interfaces"]:
                m = Metric("kubernetes_pod_network")
                m.add_tag("pod", pod["podRef"]["name"])

                for key, value in interface.items():
                    if key == "name":
                        m.add_tag("interface", value)
                        continue
                    m.add_value(key, value)
                collections.append(m)

            for container in pod["containers"]:
                m = Metric("kubernetes_pod_container")
                m.add_tag("pod", pod["podRef"]["name"])
                m.add_tag("container", container["name"])
                m.add_value(
                    "cpu_usage", self.__nano_to_deci(
                        container["cpu"]["usageNanoCores"]))

                for key, value in container["memory"].items():
                    if key == "time":
                        continue
                    m.add_value("memory_%s" % key, value)
                collections.append(m)

        return collections
