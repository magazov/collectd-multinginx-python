# collectd-multinginx-python
collectd-multinginx-python

add ```nginx.py``` to ```ModulePath``` directory and configure it in ```/etc/collectd/plugins/python.conf```

```xml
<Plugin python>
    ModulePath "/usr/share/collectd/modules"
    LogTraces "True"
    Interactive "False"
    Import "nginx"
    <Module nginx>
        www "http://localhost:80/nginx_status"
        api "http://localhost:3192/nginx_status"
    </Module>
</Plugin>
```
