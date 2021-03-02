#!/usr/bin/python3

# Copyright: (c) 2020, Randy Martinez <R.Martinez@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ceph_log_parser

short_description: ceph.log msg parser

version_added: "2.8"

description: |
    ceph_log_parser is designed to help present
    ceph cluster logs by counting the occurance
    of {{ level }} + {{ pg_line }} over
    {{ timeinternval }} in descending order.

options:
    log_file:
        description:
            - This is a path to the logfile you want analyzed.
        required: true
    level:
        default: WRN
        description:
            - type=str, choices=["DBG", "WRN"]
        required: false
    pg_line:
        default: slow request
        description:
            - type=str, choices=["slow request", "deep-scrub"]
        required: false
    timeinterval:
        default: 10
        description:
            - type=int, choices=[1, 10, 60, 1440]
        required: false

author: Randy Martinez (@utp887)
'''

EXAMPLES = r'''
# Example using vars
---
- hosts: mgmt
  vars:
    logfile_dest: "{{ playbook_dir }}/example.csv"
    search:
      - log_file: "{{ playbook_dir }}/ceph.log"
        level: "WRN"
        pg_line: "slow request"
        timeinterval: "1"
      - log_file: "{{ playbook_dir }}/ceph.log"
        level: "DBG"
        pg_line: "deep-scrub"
        timeinterval: "10"
  tasks:
  - name: Parse logs
    ceph_log_parser:
      log_file: "{{ log_file }}"
      level: "{{ level }}"
      timeinterval: "{{ timeinterval }}"
      pg_line: "{{ pg_line }}"
'''


RETURN = r'''
sorted_results:
    description: Results sorted
    type: dict
    returned: always
'''

import re
import operator
from ansible.module_utils.basic import AnsibleModule


def format_date(date):
    # reformat date to add up later 
    if timeinterval == 1:
      return "{0}".format(date[:16])
    elif timeinterval == 10:
      return "{0}0".format(date[:15])
    elif timeinterval == 60:
      return "{0}:00".format(date[:13])
    elif timeinterval == 1440:
      return "{0} 00:00".format(date[:10])

def log_split(log_file, level, pg_line, timeinterval):
    filtered_list = []
    filtered_dictionary = {}
    debug_msgs = re.findall(f'.*\[{level}\].*', open(log_file, 'r').read())
    # capture message with pg_line
    for msg in debug_msgs:
        # Find pg_line in log_file
        if f'{pg_line}' in msg:
          # Filter out linux date from first two fields separated by space
          date = " ".join(msg.split(" ", 2)[:2])
          # Create a formatted list of dates
          filtered_list.append(format_date(date))
    # Capture reformatted date count
    for reformatted_date in filtered_list:
        # Set filtered_dictionary value
        filtered_dictionary[reformatted_date] = filtered_dictionary.get(reformatted_date,0) + 1
    # Sort on count Descending
    sorted_results = dict(sorted(filtered_dictionary.items(),key=operator.itemgetter(1),reverse=True))
    # Exit module and set msg
    module.exit_json(changed=False, msg=sorted_results)

def argument_spec():
    return dict(
#            state=dict(default='present', choices=['present', 'absent'], type='str'),
            log_file=dict(type='str', required=True, help="Please provide log_file path"),
            level=dict(required=False, default="WRN", type=str, choices=["DBG", "WRN"], help="(Default: WRN)"),
            pg_line=dict(default="slow request", type=str, choices=["slow request", "deep-scrub"], help="Provide a search term"),
            timeinterval=dict(required=False, default="10", type=int, choices=[1, 10, 60, 1440], help="(Default: 10min)"),
    )

if __name__ == '__main__':
    argument_spec = argument_spec()
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    log_file = module.params['log_file']
    level = module.params['level']
    pg_line = module.params['pg_line']
    timeinterval = module.params['timeinterval']
    log_split(log_file, level, pg_line, timeinterval)
