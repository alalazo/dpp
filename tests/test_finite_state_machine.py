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
        return '{color} light on'.format(color=self.color)

    def __eq__(self, other):
        return self.color == other.color


@state.fsm(interface=SemaphoreLight)
class Semaphore(object):
    green = state.State(SemaphoreLight, 'green')
    yellow = state.State(SemaphoreLight, 'yellow')
    red = state.State(SemaphoreLight, 'red')

    slowdown = state.Event(current_state='green', next_state='yellow')
    stop = state.Event(current_state='yellow', next_state='red')
    prepare = state.Event(current_state='red', next_state='yellow')
    go = state.Event(current_state='yellow', next_state='green')

    __initial__ = yellow


class BlinkingLight(SemaphoreLight):
    def display_light(self):
        return '{color} blinking'.format(color=self.color)


def test_semaphore():
    semaphore = Semaphore()
    assert Semaphore.yellow.display_light() == 'yellow light on'
    assert semaphore.state == SemaphoreLight('yellow')
    assert semaphore.state is Semaphore.yellow
    assert semaphore.display_light() == 'yellow light on'
    semaphore('go')
    assert semaphore.state == SemaphoreLight('green')
    assert semaphore.display_light() == 'green light on'
    semaphore(Semaphore.slowdown)
    assert semaphore.state == SemaphoreLight('yellow')
    semaphore('stop')
    assert semaphore.state == SemaphoreLight('red')
    semaphore('go')  # Should do nothing from the current state
    assert semaphore.state == SemaphoreLight('red')

#def test_dynamic_changes():
#    semaphore = Semaphore()
#    semaphore.add('blinking', state.State(BlinkingLight, 'yellow'))
#    semaphore.add('blink', state.Event(current=('green', 'yellow', 'red'), next='blinking'))
#    semaphore.add('no_blink', state.Event(current='blinking', next='yellow'))
#    semaphore.commit()
