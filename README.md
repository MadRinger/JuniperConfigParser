# JuniperConfigParser
Simple helper class, which allows you to convert classic junos config into python dict and back
Usage
'''
from juniper_config_parser import JuniperConfig
a = JuniperConfig(open("router.conf"))
print(a["interfaces"])
with open("new.router.conf",wb) as f:
    for line in a.as_file():
        f.writeline(line)
'''
