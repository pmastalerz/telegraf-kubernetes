import requests


class Client:

    def __init__(self, stats_url, timeout):
        self.stats_url = stats_url
        self.timeout = timeout

    def get_stats(self):
        resp = requests.get(self.stats_url, timeout=self.timeout)
        if resp.status_code != 200:
            self.__raise_error(resp)

        return resp.json()

    def __raise_error(self, response):
        try:
            resp = response.json()
        except Exception:
            raise Exception(
                'Invalid status code, got %s, expected 200' %
                response.status_code)

            if len(resp['errors']) > 0:
                messages = ["Error: %d - %s" % (msg.code, msg.message)
                            for msg in resp['errors']]

                raise Exception(", ".join(messages))

        raise Exception(
            'Invalid status code, got %s, expected 200' %
            response.status_code)
