Ceph Log Parser
===============

Simple log parser to sort messages based on time-of-day and count.

Requirements
------------

 - Python 3.6
 - Ansible >= 2.8

Role Variables
--------------

defaults: defaults/main.yml

Dependencies
------------

Current version is designed to only run locally. Future iterations will target, OSD logs or journalctl in the case of containerized_deployment.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: mgmt
      roles:
         - { role: ceph_log_parser }

License
-------

GPL

Author Information
------------------

 - github: https://github.com/utp887
 - website: https://blog.cephtips.com/
 - linkedin: https://www.linkedin.com/in/randyjmartinez/
