import datetime
import logging
import os

from helper.exceptions import *
from .uascraping import BROWSER_HOSTS, PLATFORM_NAMES


class ReadMe:
    def __init__(self) -> None:
        self._write_io = None
        self._get_existing_lines()

    def _get_existing_lines(self):
        with open('README.md', 'r') as f:
            self._existing_lines = f.readlines()

    def _update_time_in_lines(self, item_strings, time=None):
        if isinstance(item_strings, str):
            item_strings = [item_strings, ]
        if not time:
            time = ReadMe.get_time_string()

        flag = len(item_strings)
        new_lines = self._existing_lines.copy()
        for i in range(len(new_lines)):
            for item_str in item_strings:
                if new_lines[i].find(f'Last {item_str}:') != -1:
                    flag -= 1
                    new_lines[i] = f'**Last {item_str}:** {time}  \n'
                    logging.info('Update "Last %s" time: %s', item_str, time)
                if flag == 0:
                    return new_lines
        logging.error('ReadMe time update incomplete.')

    def _get_new_ua_text(self, new_UA):
        with open(os.path.join('core', 'readme_template'), 'r') as f:
            template = f.read()

        for browser in BROWSER_HOSTS.keys():
            for platform in PLATFORM_NAMES.keys():
                template = template.replace('<--' + browser + '_' + platform + '-->', new_UA[browser][platform])

        return template

    def update_time_and_ua(self, new_UA):
        new_lines = self._update_time_in_lines(['checked', 'updated'])
        ua_text = self._get_new_ua_text(new_UA)
        with open('README.md', 'w') as f:
            for line in new_lines:
                if line.find('# Current User Agents') == -1:
                    f.write(line)
                else:
                    f.write(line)
                    break
            f.write(ua_text)
        logging.info('ReadMe updated.')

    def update_check_time(self):
        new_lines = self._update_time_in_lines(['checked', ])
        with open('README.md', 'w') as f:
            f.writelines(new_lines)
        logging.info('ReadMe updated.')

    def get_time_string():
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
