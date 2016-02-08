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

import pytest


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


@pytest.fixture
def composite_items():
    Base.counter = 0  # Make sure that the initial state is always consistent
    one = One()
    two = Two()
    return one, two


class TestCompositeUsage:
    def test_composite_from_method_list(self, composite_items):

        @composite(method_list=['add', 'subtract'])
        class CompositeFromMethodList:
            pass

        one, two = composite_items

        composite_object = CompositeFromMethodList()
        composite_object.append(one)
        composite_object.append(two)
        composite_object.add()
        assert Base.counter == 3

        composite_object.pop()
        composite_object.subtract()
        assert Base.counter == 2

    def test_composite_from_interface(self, composite_items):

        @composite(interface=Base)
        class CompositeFromInterface:
            pass

        one, two = composite_items

        composite_object = CompositeFromInterface()

        composite_object.append(one)
        composite_object.append(two)
        composite_object.add()
        assert Base.counter == 3

        composite_object.pop()
        composite_object.subtract()
        assert Base.counter == 2

class TestCompositeFailures:
    def test_wrong_container(self):
        with pytest.raises(TypeError):
            @composite(interface=Base, container=2)
            class CompositeFromInterface:
                pass


    def test_no_interface_given(self):
        with pytest.raises(TypeError):
            @composite()
            class CompositeFromInterface:
                pass
