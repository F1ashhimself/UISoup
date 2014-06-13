# !/usr/bin/env python

#    Copyright (c) 2014 Max Beloborodko.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = 'f1ashhimself@gmail.com'

from ..interfaces.i_element import IElement


class MacElement(IElement):

    _acc_role_name_map = {
        'AXWindow': u'frm',
        'AXTextArea': u'txt',
        'AXTextField': u'txt',
        'AXButton': u'btn',
        'AXStaticText': u'lbl',
        'AXRadioButton': u'rbtn',
        'AXSlider': u'sldr',
        'AXCell': u'tblc',
        'AXImage': u'img',
        'AXToolbar': u'tbar',
        'AXScrollBar': u'scbr',
        'AXMenuItem': u'mnu',
        'AXMenu': u'mnu',
        'AXMenuBar': u'mnu',
        'AXMenuBarItem': u'mnu',
        'AXCheckBox': u'chk',
        'AXTabGroup': u'ptl',
        'AXList': u'lst',
        'AXMenuButton': u'cbo',
        'AXRow': u'tblc',
        'AXColumn': u'col',
        'AXTable': u'tbl',
        'AXScrollArea': u'sar',
        'AXOutline': u'otl',
        'AXValueIndicator': u'val',
        'AXDisclosureTriangle': u'dct',
        'AXGroup': u'grp',
        'AXPopUpButton': u'pubtn',
        'AXApplication': u'app',
        'AXDocItem': u'doc',
        'AXHeading': u'tch',
        'AXGenericElement': u'gen'
    }

    def __init__(self, obj_selector, process_id):
        """
        Constructor.

        Arguments:
            - obj_selector: string, object selector.
            - process_id: int, process id.
        """

        self._object_selector = obj_selector
        self._process_id = process_id

    def click(self, x_offset=None, y_offset=None):
        pass

    def right_click(self, x_offset=None, y_offset=None):
        pass

    def double_click(self, x_offset=None, y_offset=None):
        pass

    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        pass

    def check_state(self, state):
        pass

    def proc_id(self):
        return self._process_id

    def is_top_level_window(self):
        pass

    def is_selected(self):
        pass

    def is_pressed(self):
        pass

    def is_checked(self):
        pass

    def is_visible(self):
        pass

    def is_enabled(self):
        pass

    def acc_parent_count(self):
        pass

    def acc_child_count(self):
        pass

    def acc_role(self):
        pass

    def acc_name(self):
        pass

    def set_name(self, name):
        pass

    def set_focus(self):
        pass

    def acc_c_name(self):
        pass

    def acc_location(self):
        pass

    def acc_value(self):
        pass

    def set_value(self, value):
        pass

    def acc_description(self):
        pass

    def acc_parent(self):
        pass

    def acc_selection(self):
        pass

    def acc_state(self):
        pass

    def acc_focus(self):
        pass

    def acc_select(self, i_selection):
        pass

    def acc_role_name(self):
        pass

    def __iter__(self):
        pass

    def find(self, only_visible=True, **kwargs):
        pass

    def findall(self, only_visible=True, **kwargs):
        pass

    def is_object_exists(self, **kwargs):
        pass

    def toxml(self):
        pass
