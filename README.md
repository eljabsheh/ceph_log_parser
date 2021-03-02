Ceph Log Parser
===============

Simple ceph.log parser to sort messages based on time-of-day and count. Future iterations will present warnings and recommendtions based on findings.

Requirements
------------

 - Python 3.6
 - Ansible >= 2.8

Environment Setup
-----------------

(Optional) Create a virtual environment: 

```
  # Clone Repo and cd into the directory
  git clone https://github.com/utp887/ceph_log_parser.git && cd ceph_log_parser
  # Create virtual environment
  python3.6 -m venv venv
  # Activate venv & install requirements
  . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt 
```

Run example playbook:

```
  ansible-playbook log_parser.playbook.sample
```

Review generated .csv:
```
  cat "{{ inventory_dir }}"/example.csv
```

Dependencies
------------

Current version is designed to only run locally. Future iterations will target, remote nodes.

Module Documentation
--------------------

```
  ansible-doc ceph_log_parser
```

License
-------

GPL

Author Information
------------------

 - github: https://github.com/utp887
 - website: https://blog.cephtips.com/
 - linkedin: https://www.linkedin.com/in/randyjmartinez/
