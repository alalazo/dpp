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


class SemaphoreLight(object):
    def __init__(self, color):
        self.color = color

    def display_light(self):
        print('{color} light on'.format(color=self.color))


@state.fsm(interface=SemaphoreLight)
class Semaphore(object):
    green = state.State(SemaphoreLight, 'green')
    yellow = state.State(SemaphoreLight, 'yellow')
    red = state.State(SemaphoreLight, 'red')

    slowdown = state.Event(current='green', next='yellow')
    stop = state.Event(current='yellow', next='red')
    prepare = state.Event(current='red', next='yellow')
    go = state.Event(current='yellow', next='green')


class BlinkingLight(SemaphoreLight):
    def display_light(self):
        print('{color} blinking'.format(color=self.color))


def test_semaphore():
    semaphore = Semaphore()
    assert semaphore.state == SemaphoreLight('yellow')
    semaphore.handle('go')


def test_dynamic_changes():
    semaphore = Semaphore()
    semaphore.add('blinking', state.State(BlinkingLight, 'yellow'))
    semaphore.add('blink', state.Event(current=('green', 'yellow', 'red'), next='blinking'))
    semaphore.add('no_blink', state.Event(current='blinking', next='yellow'))
    semaphore.commit()

