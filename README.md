# bind-notify

![Logo](https://i.imgur.com/GMYC4Qm.png)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/aelth/bind-notify/blob/main/LICENSE) [![Python 3.x](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)

Very simple *Python 3* script that monitors [BIND](https://www.isc.org/bind/) logs and sends [Telegram](https://telegram.org/) notifications if log entry/line matches a preconfigured regex.

This script was created when a configuration error on secondary DNS server ([TSIG](https://en.wikipedia.org/wiki/TSIG) key mismatch) caused inability to transfer zone to secondary server and, eventually, the expiry of the zone that was not noticed until the other problems emerged.

It became obvious that the script can be generalized and used for monitoring of all kinds of errors and events in *BIND* logs that you would like to know about - for example, failed zone transfers, DNSSEC errors, etc.

# Installation

*bind-notify* depends on two additional packages:
- [pygtail](https://pypi.org/project/pygtail/)
- [telegram-send](https://pypi.org/project/telegram-send/)

Install them using `pip` directly, or using the provided *requirements.txt* file (recommended inside the *virtualenv*):
```
pip install telegram-send
pip install pygtail

OR

pip install -r requirements

```

# Usage

Before the script can be used, provided *settings.conf.example* and *telegram.conf.example* must be renamed to *settings.conf/telegram.conf* respectively and edited.

*settings.conf* file specifies *BIND* log files that need to be monitored, along with the regular expressions that determine the line/log entry of interest.  
The file is well documented and self-explanatory.

*telegram.conf* file specifies chat details (*token* and *chat id*) that determine the channel where the notifications will be sent.  
Configuration can be generated using the config "wizard", embedded in *telegram-send*:
```
telegram-send --configure

OR

telegram-send --configure-group
```

After configuration is complete, run the script directly, or start it automatically using *systemd*, using the provided *systemd* config file (be sure to modify the file according to your needs).
