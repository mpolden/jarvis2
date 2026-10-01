from email.utils import mktime_tz, parsedate_tz
from xml.etree import ElementTree as etree

import requests

from jobs import AbstractJob


class Rss(AbstractJob):
    def __init__(self, conf):
        self.url = conf["url"]
        self.title = conf.get("title")
        self.interval = conf["interval"]
        self.timeout = conf.get("timeout")

    def _parse(self, xml):
        tree = etree.fromstring(xml.encode("utf-8"))
        items = []
        for item in tree.findall("./channel/item"):
            title = getattr(item.find("title"), "text", None)
            pubDate = getattr(item.find("pubDate"), "text", None)
            if title is None or pubDate is None:
                continue
            time = mktime_tz(parsedate_tz(pubDate))
            items.append({"title": title, "time": time})
        title = self.title
        if title is None:
            title = tree.find("./channel/title").text
        return {"title": title, "items": items}

    def get(self):
        r = requests.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        return self._parse(r.text)
