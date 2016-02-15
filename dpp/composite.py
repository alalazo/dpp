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
"""
Everything you need to employ the composite pattern
"""
from __future__ import absolute_import, print_function

import inspect
import collections
import functools

from .inspection import is_private, is_special


def composite(interface=None, method_list=None, container=list):
    """
    Returns a class decorator that patches a class adding all the methods it needs to be a composite for a given
    interface.

    :param interface: class exposing the interface to which the composite object must conform. Only non-private and
    non-special methods will be taken into account
    :param method_list: names of methods that should be part of the composite
    :param container: container for the composite object (default = list). Must fulfill the MutableSequence contract.
    The composite class will expose the container API to manage object composition
    :return: class decorator
    """
    # Check if container fulfills the MutableSequence contract and raise an exception if it doesn't
    # The patched class returned by the decorator will inherit from the container class to expose the
    # interface needed to manage objects composition
    if not inspect.isclass(container) or not issubclass(container, collections.MutableSequence):
        raise TypeError("Container must fulfill the MutableSequence contract")

    # Check if at least one of the 'interface' or the 'method_list' arguments are defined
    if interface is None and method_list is None:
        raise TypeError("Either 'interface' or 'method_list' must be defined on a call to composite")

    def cls_decorator(cls):
        # pylint: disable=missing-docstring
        # Retrieve the base class of the composite. Inspect its methods and decide which ones will be overridden
        def no_special_no_private(mthd):
            # Here we have a nasty difference between python 2 and python 3.
            # In python 2 x is considered to be an unbound method when coming from a class
            # (ismethod(x) == True, isfunction(x) == False)
            # In python 3 x is considered just a function when coming from a class
            # (ismethod(x) == False, isfunction(x) == True)
            return not is_special(mthd) and not is_private(mthd)

        # Patch the behavior of each of the methods in the previous list. This is done associating an instance of the
        # descriptor below to any method that needs to be patched.
        class IterateOver(object):
            """
            Descriptor used to patch methods in a composite. It iterates over all the items in the instance containing
            the associated attribute and calls for each of them an attribute with the same name
            """

            # pylint: disable=too-few-public-methods
            def __init__(self, name, func=None):
                self.name = name
                self.func = func

            def __get__(self, instance, owner):
                def getter(*args, **kwargs):
                    for item in instance:
                        getattr(item, self.name)(*args, **kwargs)
                # If we are using this descriptor to wrap a method from an interface, then we must conditionally
                # use the `functools.wraps` decorator to set the appropriate fields.
                if self.func is not None:
                    getter = functools.wraps(self.func)(getter)
                return getter

        dictionary_for_type_call = {}
        # Construct a dictionary with the methods explicitly passed as name
        if method_list is not None:
            # python@2.7: method_list_dict = {name: IterateOver(name) for name in method_list}
            method_list_dict = {}
            for name in method_list:
                method_list_dict[name] = IterateOver(name)
            dictionary_for_type_call.update(method_list_dict)
        # Construct a dictionary with the methods inspected from the interface
        if interface is not None:
            # If an interface is passed, class methods and static methods should not be inserted in the list
            # of methods to be wrapped
            interface_methods = inspect.classify_class_attrs(interface)  # Get all the class attributes
            interface_methods = [x for x in interface_methods if x.kind == 'method']  # Select only methods
            interface_methods = [x for x in interface_methods if no_special_no_private(x.object)]
            # {name: IterateOver(name, method) for name, method in interface_methods.items()}
            interface_methods_dict = dict(
                (item.name, IterateOver(item.name, item.object)) for item in interface_methods
            )
            dictionary_for_type_call.update(interface_methods_dict)
        # Get the methods that are defined in the scope of the composite class and override any previous definition

        # {name: method for name, method in inspect.getmembers(cls, predicate=inspect.ismethod)}
        #cls_method = inspect.classify_class_attrs(cls)
        #cls_method = [x for x in cls_method if x.kind == 'method']
        cls_method = {}
        for name, method in inspect.getmembers(
                cls,
                predicate=lambda item: inspect.ismethod(item) or inspect.isfunction(item)):
            cls_method[name] = method

        dictionary_for_type_call.update(cls_method)
        # Generate the new class on the fly and return it
        # TODO : inherit from interface if we start to use ABC classes?
        wrapper_class = type(cls.__name__, (cls, container), dictionary_for_type_call)
        return wrapper_class

    return cls_decorator
