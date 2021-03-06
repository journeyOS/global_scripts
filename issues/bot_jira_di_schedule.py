#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2020 anqi.huang@outlook.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import optparse
import os
import threading
import time
import schedule
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from base.smart_log import smart_log
from issues.bot_jira_di import BotJiraDI

project = "all"
who = "bot_owner"
auto = False

bot_jira_dI = BotJiraDI()


def parseargs():
    usage = "usage: %prog [options] arg1 arg2"
    parser = optparse.OptionParser(usage=usage)

    option_group = optparse.OptionGroup(parser, "auto send di message options")

    option_group.add_option("-p", "--project", dest="project", default="all", help="which di project")
    option_group.add_option("-w", "--who", dest="who", default="bot_owner", help="send to who")
    option_group.add_option("-a", "--auto", dest="auto", default=False, action="store_true",
                            help="auto send di message")

    parser.add_option_group(option_group)

    (options, args) = parser.parse_args()

    return (options, args)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def di_job():
    bot_jira_dI.send_di(project, who)


def main():
    smart_log(os.path.abspath(__file__))
    (options, args) = parseargs()
    global project
    project = options.project.strip()
    global who
    who = options.who.strip()
    global auto
    auto = options.auto
    smart_log("bot project = %s, who = %s, auto = %d " % (project, who, auto))
    di_job()

    if auto:
        schedule.every(5).seconds.do(run_threaded, di_job)
        for i in ["10:00", "17:30"]:
            schedule.every().monday.at(i).do(run_threaded, di_job)
            schedule.every().tuesday.at(i).do(run_threaded, di_job)
            schedule.every().wednesday.at(i).do(run_threaded, di_job)
            schedule.every().thursday.at(i).do(run_threaded, di_job)
            schedule.every().friday.at(i).do(run_threaded, di_job)

    return 0


if __name__ == "__main__":
    main()
    while auto:
        schedule.run_pending()
        time.sleep(5)
