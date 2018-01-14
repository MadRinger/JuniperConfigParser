# JuniperConfigParser
Simple helper class, which allows you to convert classic junos config into python dict and back
Usage

```
from juniper_config_parser import JuniperConfig
a = JuniperConfig(open("router.conf"))
print(a["interfaces"])
with open("new.router.conf",wb) as f:
    for line in a.as_file():
        f.writeline(line)
```

set_commands and as_file with sections

As far as we are working with dicts, there is really no way to determine intend level or prefix, when it directly passed
. To perform export on individual section, specify intend/prefix to call as

```
a = JuniperConfig(open("router.conf"))
for line in a.set_commands(["interfaces"],"interfaces"):
    print(line)
```