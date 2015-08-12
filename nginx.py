#! /usr/bin/env python


import re
import urllib2

import collectd


class Nginx(object):
    def __init__(self):
        self.pattern = re.compile("([A-Z][\w]*).+?(\d+)")
        self.urls = {}

    def do_nginx_status(self):
        for instance, url in self.urls.items():
            try:
                response = urllib2.urlopen(url)
            except urllib2.HTTPError, e:
                collectd.error(str(e))
            except urllib2.URLError, e:
                collectd.error(str(e))
            else:
                data = response.read()
                m = self.pattern.findall(data)
                for key, value in m:
                    metric = collectd.Values()
                    metric.plugin = 'nginx-%s' % instance
                    metric.type_instance = key.lower()
                    metric.type = 'nginx_connections'
                    metric.values = [value]
                    metric.dispatch()

                requests = data.split('\n')[2].split()[-1]
                collectd.debug('Requests %s' % requests)
                metric = collectd.Values()
                metric.plugin = 'nginx-%s' % instance
                metric.type = 'nginx_requests'
                metric.values = [requests]
                metric.dispatch()

    def config(self, obj):
        self.urls = dict((self.urls[node.key], node.values[0]) for node in obj.children)


nginx = Nginx()
collectd.register_config(nginx.config)
collectd.register_read(nginx.do_nginx_status)
