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

from dpp import composite


class Base(object):
    counter = 0

    def add(self):
        raise NotImplemented('add not implemented')

    def subtract(self):
        raise NotImplemented('subtract not implemented')


class One(Base):
    def add(self):
        Base.counter += 1

    def subtract(self):
        Base.counter -= 1


class Two(Base):
    def add(self):
        Base.counter += 2

    def subtract(self):
        Base.counter -= 2


def test_composite_from_method_list():

    @composite(method_list=['add', 'subtract'])
    class CompositeFromMethodList:
        pass

    composite_object = CompositeFromMethodList()
    composite_object.append(One())
    composite_object.append(Two())
    composite_object.add()
    assert Base.counter == 3
    composite_object.pop()
    composite_object.subtract()
    assert Base.counter == 2


def test_composite_from_interface():

    @composite(interface=Base)
    class CompositeFromInterface:
        pass

    composite_object = CompositeFromInterface()

    composite_object.append(One())
    composite_object.append(Two())
    composite_object.add()
    assert Base.counter == 3

    composite_object.pop()
    composite_object.subtract()
    assert Base.counter == 2

def test_error_conditions():

    def wrong_container():
        @composite(interface=self.Base, container=2)
        class CompositeFromInterface:
            pass

    def no_methods():
        @composite()
        class CompositeFromInterface:
            pass

    #self.assertRaises(TypeError, wrong_container)
    #self.assertRaises(TypeError, no_methods)
