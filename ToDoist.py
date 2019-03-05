#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pytodoist import todoist
import datetime

def ConvTime(hour,min):
    today = datetime.date.today().strftime("%Y-%m-%d")
    time = today + "T" + str(hour).zfill(2) +":"+str(min).zfill(2)
    return time

def login():
    return todoist.login_with_api_token(os.environ['TODOIST_API_TOKEN'])