# -*- coding: utf-8 -*-
#
# Copyright 2016 Massimiliano Culpo
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
"""Provides the expected descriptor"""


class Expected(object):
    """Descriptor that holds a value or the exception explaining
    why the value was not set
    """

    # pylint: disable=too-few-public-methods
    def __init__(self,
                 predicate,
                 exc_cls=RuntimeError,
                 message='Invalid value set',
                 trigger_on_set=False):
        """
        Initializes the descriptor with the predicate and optional information

        :param predicate: predicate used to validate the value to be held
        :param exc_cls: class of the exception that will be raised is the predicate returns False
        :param message: exception message
        :param trigger_on_set: whether or not to trigger the exception when the value is set
        """
        self.predicate = predicate
        self.exc_cls = exc_cls
        self.message = message
        self.trigger_on_set = trigger_on_set
        self.value = None

    def _check_predicate(self, instance):
        if not self.predicate(self.value):
            self.message += '\n\ttriggered from instance {0}'.format(repr(instance))
            raise self.exc_cls(self.message.format(**self.__dict__))

    def __get__(self, instance, owner):
        self._check_predicate(instance)
        return self.value

    def __set__(self, instance, value):
        self.value, old_value = value, self.value
        if self.trigger_on_set:
            try:
                self._check_predicate(instance)
            except TypeError:
                # Reset the old value in case client
                # wants to manage the exception
                self.value = old_value
                raise
