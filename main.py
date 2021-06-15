#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: The Soloist
# @Time: 2021-06-02 08:20:59
# @File: /main.py
# @Description:

import sys
import configparser
from pathlib import Path
from notion2md.export_manager import export_cli


work_path = Path(__file__).parent
ini_path = work_path / "config.ini"

try:
    conf = configparser.ConfigParser()
    conf.read(ini_path, encoding="utf-8")
    token = conf.get('notion', 'token_v2')
except Exception as e:
    print("%s is not exist or token_v2 is null." % ini_path, e)
    conf.clear()
    conf.add_section('notion')
    token = input("Please input your token: ").strip()
    conf.set('notion', 'token_v2', token)
    conf.write(open(ini_path, 'w'))


if __name__ == "__main__":
    # print(sys.argv)
    url = sys.argv[1] if len(sys.argv) == 2 else None
    export_cli(token_v2=token, url=url, bmode=False)
