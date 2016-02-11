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

from dpp import inspection


def test_is_private_and_is_special():
    def _foo_():
        pass

    def __foo():
        pass

    def _foo():
        pass

    def ___foo__():
        pass

    def __foo__():
        pass

    def bar():
        pass

    # Checks expected values of is_private
    assert inspection.is_private(_foo_) == True
    assert inspection.is_private(_foo) == True
    assert inspection.is_private(__foo) == True
    assert inspection.is_private(___foo__) == True
    assert inspection.is_private(__foo__) == False  # FIXME : expected false negative
    assert inspection.is_private(bar) == False

    # Checks expected values of is_private
    assert inspection.is_special(_foo_) == False
    assert inspection.is_special(_foo) == False
    assert inspection.is_special(__foo) == False
    assert inspection.is_special(___foo__) == False
    assert inspection.is_special(__foo__) == True  # FIXME : expected false positive
    assert inspection.is_special(bar) == False
