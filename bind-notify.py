#!/usr/bin/env python3

import json
import os
import re
import sys
import telegram_send
import time

from pygtail import Pygtail
from configparser import ConfigParser

def print_err(msg):
    print('\033[91m[-] ' + msg + '\033[0m')


def print_warn(msg):
    print('\033[93m[!] ' + msg + '\033[0m')


def print_succ(msg):
    print('\033[92m' + msg + '\033[0m')


# influenced by ARTLAS: https://github.com/mthbernardes/ARTLAS
class Notifier(object):
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            print_err(f'Config file {config_file} does not exist! Please check the path to configuration file...')
            sys.exit(1)

        print_succ(f'Reading config file {config_file}...')
        self.parse_config(config_file)
        print_succ(f'Configuration file parsed successfully!')

    def parse_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)

        self.conf = dict()
        # general settings
        self.conf['logs'] = config.get('General', 'logs').split(',')
        self.conf['sleep'] = int(config.get('General', 'sleep'))

        for log in self.conf['logs']:
            section_name = 'Log-' + log
            if not config.has_section(section_name):
                print_warn(f'Section {section_name} does not exist in config file! Please check the syntax...')
                continue
            
            self.conf['file-' + log] = config.get(section_name, 'log')
            self.conf['rex-' + log] = re.compile(config.get(section_name, 'rex'))

        # telegram settings
        self.conf['telegram_config'] = config.get('Telegram', 'conf')

    def start(self):
        # run in endless loop, waiting for n seconds
        while True:
            try:
                for log in self.conf['logs']:
                    for line in Pygtail(self.conf['file-' + log], read_from_end=True):
                        denied_axfr = self.conf['rex-' + log].search(line)
                        if denied_axfr:
                            ip = denied_axfr[1]
                            zone = denied_axfr[2]
                            print(f'Denied or bad AXFR for {zone}</b> from {ip}!')

                            # send telegram notification
                            telegram_send.send(conf=self.conf['telegram_config'], parse_mode='html', messages=[f'⚠️ Denied or bad AXFR for <b>{zone}</b> from <b>{ip}</b>!'])

                time.sleep(self.conf['sleep'])
                    
            except KeyboardInterrupt:
                print_warn('Received CTRL+C, exiting...')
                return
            except Exception as e:
                print_err(f'Error while running the program: {e}')
                return


if __name__ == '__main__':
	notifier = Notifier('./settings.conf')
	notifier.start()
