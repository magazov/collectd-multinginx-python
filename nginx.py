#! /usr/bin/env python


import collectd
import re
import urllib2

class NutcrackerServer( object ):
    def __init__(self):
        self.pattern = re.compile("([A-Z][\w]*).+?(\d+)")
        self.urls = {}


    def do_nginx_status( self ):
        for instance, url in self.urls.iteritems():
            try:
                response = urllib2.urlopen(url)
            except urllib2.URLError, e:
                collectd.error(str(e))
            except urllib2.HTTPError, e:
                collectd.error(str(e))
            else:
                data = response.read()
                m = self.pattern.findall(data)
                collectd.info(repr(m))
                for key, value in m:
                    metric = collectd.Values()
                    metric.plugin = 'nginx-%s'%instance
                    metric.type_instance = key.lower()
                    metric.type = 'nginx_connections'
                    metric.values = [value]
                    metric.dispatch()
                con = data.split('\n')[2].split()[-1]
                collectd.info('Requests %s'%con)
                metric = collectd.Values()
                metric.plugin = 'nginx-%s'%instance
                metric.type = 'nginx_requests'
                metric.values = [con]
                metric.dispatch()


    def config(self, obj):
        for node in obj.children:
            self.urls[node.key] = node.values[0]

nginx = NutcrackerServer()
collectd.register_config(nginx.config)
collectd.register_read(nginx.do_nginx_status)
