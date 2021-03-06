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

import datetime
import os
import optparse
import platform


def _smart_log(message):
    print("%s -> %s" % (datetime.datetime.now(), message))


def check_env():
    if 'ANDROID_HOME' in os.environ:
        return True
    else:
        print("export ANDROID_HOME=/work/solo/tools/sdk/")
        return False


def is_linux():
    plt = platform.system()
    _smart_log("system = %s " % plt)
    if plt == "Linux":
        return True
    else:
        return False


def elapsed_interval(start, end):
    elapsed = end - start
    min, secs = divmod(elapsed.days * 86400 + elapsed.seconds, 60)
    hour, minutes = divmod(min, 60)
    return '%.2d:%.2d:%.2d' % (hour, minutes, secs)


def parseargs(linux):
    usage = "usage: %prog [options] arg1 arg2"
    parser = optparse.OptionParser(usage=usage)

    gradle_default = "./gradlew"
    threads = 32
    if linux:
        gradle_default = "/work/solo/tools/gradle/gradle-6.3/bin/gradle"
        threads = 128

    option_group = optparse.OptionGroup(parser, "gradle build app options")

    option_group.add_option("-g", "--gradle", dest="gradle",
                            help="which gradle want to build",
                            default=gradle_default)
    option_group.add_option("-t", "--type", dest="type",
                            help="what type want to build", default="assembleRelease")
    option_group.add_option("-j", "--threads", dest="threads",
                            help="how threads want to build", default=str(threads))

    parser.add_option_group(option_group)

    (options, args) = parser.parse_args()

    return (options, args)


def main_impl(linux):
    (options, args) = parseargs(linux)
    build_gradle = options.gradle.strip()
    build_type = options.type.strip()
    build_threads = options.threads.strip()
    cmd = "%s --no-build-cache %s --daemon --configure-on-demand --parallel --max-workers=%s" % (
        build_gradle, build_type, build_threads)
    _smart_log(cmd)
    start_time = datetime.datetime.now()
    os.system(cmd)
    end_time = datetime.datetime.now()
    total_time = elapsed_interval(start_time, end_time)
    _smart_log("build time = %s" % total_time)
    # if linux is not True:
    #     cmd_install = "adb install -r -d " + os.getcwd() + "/build/out_product_branch/I19tService_hta_unsigned.apk"
    #     _smart_log(cmd_install)
    #     os.system(cmd_install)


def main():
    _smart_log(os.path.abspath(__file__))
    if is_linux():
        if check_env():
            main_impl(True)
    else:
        main_impl(False)

    return 0


if __name__ == "__main__":
    main()
