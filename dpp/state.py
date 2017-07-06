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
"""State pattern and common variations"""
import inspect


class State(object):
    """Wrap the data for the current state and aggregate the information on transitions
    to the next states.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, cls, *args):
        self.data = cls(*args)  # Wrapped object that will act as a state
        self.transitions = {
        }  # Transitions from this to other states in the form {event : next_state}

    def __getattr__(self, item):
        """If the attribute is not defined in the wrapper, delegate to the wrapped object.

        :param item: attribute requested
        :return: the attribute if it exists
        """
        return getattr(self.data, item)

    def next_state(self, event):
        """
        If a transition associated with the event exists, return the next state otherwise None

        :param event: event name or Event instance
        :return: next state or None
        """
        return self.transitions.get(event)


class Event(object):
    """
    Represent an event that triggers a transition in the finite state machine
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, current_state, next_state):
        self.current = current_state
        self.next = next_state


class FiniteStateMachineBase(object):
    """
    Operations that are added to all finite state machines
    """

    # pylint: disable=too-few-public-methods
    def __call__(self, event):
        """
        Handle transitions triggered by events.

        If an event triggers a transition the state will be changed.

        :param event: event name or Event instance
        """
        # pylint: disable=access-member-before-definition
        # pylint: disable=attribute-defined-outside-init
        event = self.events[event] if not isinstance(event, Event) else event
        next_state = self.state.next_state(event)
        if next_state is not None:
            self.state = next_state

    def __getattr__(self, name):
        """
        Delegates unknown methods to the current state

        :param name: name of the method to be forwarded
        :return: whatever returned by the method
        """
        return getattr(self.state, name)


def fsm(interface=None, method_list=None):
    """
    Decorates (patches) a class to construct a finite state machine.

    Either interface or method_list or both should be given.

    :param interface: class providing the interface of the fsm state
    :param method_list: list of methods that each state should provide

    :return: class patched to be a finite state machine
    """

    # Check if at least one of the 'interface' or the 'method_list' arguments are defined
    if interface is None and method_list is None:
        raise TypeError("Either 'interface' or 'method_list' must be defined on a call to fsm")

    def cls_decorator(cls):
        """
        Decorator that patches a class to add finite state machine operations.

        :param cls: class to be patched

        :return: finite state machine
        """
        # The patched class should intercept all the State and Event attributes and :
        # - store type and arguments of states
        # - event transitions in the starting state
        # - add a few methods that will be common to fsm ('handle(event)', 'state', ...)
        # - delegate to self.state for calls to methods that are part of the state interface

        # Initialize quantities
        bases = (cls, FiniteStateMachineBase)  # Base classes for Finite State Machine
        additional_attributes = {}  # Dictionary of additional attributes
        cls_attributes = inspect.classify_class_attrs(cls)  # Class attributes
        # Check the initial state
        fsm_states = dict((item.name, item.object)
                          for item in cls_attributes if isinstance(item.object, State))
        fsm_events = dict((item.name, item.object)
                          for item in cls_attributes if isinstance(item.object, Event))
        additional_attributes['state'] = fsm_states.pop('__initial__')
        additional_attributes['states'] = fsm_states
        additional_attributes['events'] = fsm_events
        # Check states interface
        for _, event in fsm_events.items():
            current_state = event.current
            next_state = event.next
            # Check that the states exists
            fsm_states[current_state].transitions[event] = fsm_states[next_state]

        return type(cls.__name__, bases, additional_attributes)

    return cls_decorator
