# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for DeleteIngressRule
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-appengine-admin


# [START appengine_generated_appengine_admin_v1_Firewall_DeleteIngressRule_sync]
from google.cloud import appengine_admin_v1


def sample_delete_ingress_rule():
    # Create a client
    client = appengine_admin_v1.FirewallClient()

    # Initialize request argument(s)
    request = appengine_admin_v1.DeleteIngressRuleRequest(
    )

    # Make the request
    response = client.delete_ingress_rule(request=request)


# [END appengine_generated_appengine_admin_v1_Firewall_DeleteIngressRule_sync]
