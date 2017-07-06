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

    @classmethod
    def reset(cls):
        cls.counter = 0

    def add(self):
        raise NotImplemented('add not implemented')

    def subtract(self):
        raise NotImplemented('subtract not implemented')

    @staticmethod
    def get_number():
        return Base.counter


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
    Base.reset()  # Make sure that the initial state is always consistent
    one = One()
    two = Two()
    return one, two


class TestCompositeUsage:
    def test_composite_from_method_list(self, composite_items):
        @composite(method_list=['add', 'subtract'])
        class CompositeFromMethodList(object):
            @staticmethod
            def get_number():
                return 0

        one, two = composite_items

        composite_object = CompositeFromMethodList()
        composite_object.append(one)
        composite_object.append(two)
        composite_object.add()
        assert Base.counter == 3

        composite_object.pop()
        composite_object.subtract()
        assert Base.counter == 2

        assert CompositeFromMethodList.get_number() == 0

    def test_composite_from_interface(self, composite_items):
        @composite(interface=Base)
        class CompositeFromInterface(object):
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

        assert CompositeFromInterface.get_number() == 2
        assert isinstance(composite_object, Base)
        assert issubclass(CompositeFromInterface, Base)

    def test_get_item(self, composite_items):
        @composite(interface=Base)
        class CompositeFromInterface(object):
            pass

        one, two = composite_items
        composite_object = CompositeFromInterface()

        composite_object.append(one, 'one')
        composite_object.append(two, 'two')

        # Check indexed access
        assert composite_object[0] is one
        assert composite_object[1] is two

        # Check access by name
        assert composite_object['one'] is one
        assert composite_object['two'] is two

        # Check contains
        assert one in composite_object
        assert two in composite_object
        assert 'one' in composite_object
        assert 'two' in composite_object

        # Check assignment
        composite_object[:] = [two, one]

        assert composite_object[0] is two
        assert composite_object[1] is one
        assert composite_object['one'] is one
        assert composite_object['two'] is two

        composite_object[:] = [two, two]

        assert composite_object[0] is two
        assert composite_object[1] is two
        assert 'one' not in composite_object
        assert composite_object['two'] is two

        # Check deletion

        assert len(composite_object) == 2

        del composite_object[0]

        assert len(composite_object) == 1
        assert composite_object[0] == two
        assert 'two' in composite_object

        del composite_object[0]

        assert len(composite_object) == 0
        assert 'two' not in composite_object


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
