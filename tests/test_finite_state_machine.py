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

from dpp import state

import abc
import future.utils


class SemaphoreLight(future.utils.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def display_light(self):
        pass


@state.fsm(interface=SemaphoreLight)
class Semaphore(object):
    @staticmethod
    def state(obj):
        return obj

    @staticmethod
    def event(current, next):
        def decorator(func):
            return func
        return decorator

@Semaphore.state
class GreenLight(SemaphoreLight):
    def display_light(self):
        print('Green light')


@Semaphore.state
class YellowLight(SemaphoreLight):
    def display_light(self):
        print('Yellow light')


@Semaphore.state
class RedLight(SemaphoreLight):
    def display_light(self):
        print('Red light')


@Semaphore.event(current=GreenLight, next=YellowLight)
class SlowDown(object):
    pass


semaphore = Semaphore()

#semaphore.handle(SlowDown())
