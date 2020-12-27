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


import json
import os


class JiraReviewConfig(object):
    def __init__(self, json_config):
        self.jira_jql_review = json_config["jira_jql_review"]

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        print(['%s:%s' % item for item in self.__dict__.items()])

    @staticmethod
    def get_configs():
        path = os.path.join(os.path.dirname(__file__), ".jira_review.json")
        with open(path, 'r') as f:
            json_config = json.loads(f.read())
            config = JiraReviewConfig(json_config)

        return config
