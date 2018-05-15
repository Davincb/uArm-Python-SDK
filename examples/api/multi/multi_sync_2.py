#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, UFactory, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
from uarm.tools.list_ports import get_ports


"""
连接所有过滤到的串口，并同步运动
"""

swift_list = []
ports = get_ports(filters={'hwid': 'USB VID:PID=2341:0042'})
for port in ports:
    swift_list.append(SwiftAPI(port=port['device']))

for swift in swift_list:
    swift.waiting_ready()


def multi_swift_cmd(cmd, *args, **kwargs):
    wait = kwargs.pop('wait', False)
    timeout = kwargs.get('timeout', None)
    for swift in swift_list:
        swift_cmd = getattr(swift, cmd)
        swift_cmd(*args, **kwargs, wait=False)
    if wait:
        for swift in swift_list:
            swift.flush_cmd(timeout)


while True:
    multi_swift_cmd('set_position', x=200, y=0, z=100, speed=10000, wait=True, timeout=30)
    multi_swift_cmd('set_position', x=200, y=100, z=100, speed=10000, wait=True, timeout=30)
    multi_swift_cmd('set_position', x=200, y=-100, z=100, speed=10000, wait=True, timeout=30)
    multi_swift_cmd('set_position', x=200, y=0, z=150, speed=10000, wait=True, timeout=30)




