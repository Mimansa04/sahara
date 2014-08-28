# Copyright 2011 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# It's based on debug middleware from oslo-incubator

"""Debug middleware"""

from __future__ import print_function
import sys

import webob.dec

from sahara.openstack.common.middleware import base


class LogExchange(base.Middleware):
    """Helper class that returns debug information.

    Can be inserted into any WSGI application chain to get information about
    the request and response.
    """

    @webob.dec.wsgify
    def __call__(self, req):
        print(("*" * 40) + " REQUEST ENVIRON")
        for key, value in req.environ.items():
            print(key, "=", value)
        if req.is_body_readable:
            print(('*' * 40) + " REQUEST BODY")
            if req.content_type == 'application/json':
                print(req.json)
            else:
                print(req.body)
        print()

        resp = req.get_response(self.application)

        print(("*" * 40) + " RESPONSE HEADERS")
        for (key, value) in resp.headers.iteritems():
            print(key, "=", value)
        print()

        resp.app_iter = self.print_generator(resp.app_iter)

        return resp

    @staticmethod
    def print_generator(app_iter):
        """Prints the contents of a wrapper string iterator when iterated."""
        print(("*" * 40) + " RESPONSE BODY")
        for part in app_iter:
            sys.stdout.write(part)
            sys.stdout.flush()
            yield part
        print()