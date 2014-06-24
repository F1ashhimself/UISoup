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
from ..utils.mac_utils import MacUtils
from .. import TooSaltyUISoupException


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

    def __init__(self, obj_selector, layer_num, process_name, process_id):
        """
        Constructor.

        Arguments:
            - obj_selector: string, object selector.
            - layer_num: int, layer number. I.e. main window will be layer 0.
            - process_name: string, process
            - process_id: int, process id.
        """

        self._object_selector = obj_selector
        self._layer_num = layer_num
        self._proc_id = process_id
        self._proc_name = process_name
        self._cache = set()

    @property
    def _properties(self):
        """
        Property for element properties.
        """

        properties = MacUtils.ApplescriptExecutor.get_element_properties(
            self._object_selector, self._proc_name)

        return properties

    @property
    def _role(self):
        """
        Property for element role.
        """

        return self._properties.get('AXRole', None)

    def click(self, x_offset=None, y_offset=None):
        pass

    def right_click(self, x_offset=None, y_offset=None):
        pass

    def double_click(self, x_offset=None, y_offset=None):
        pass

    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        pass

    @property
    def proc_id(self):
        return self._proc_id

    @property
    def is_top_level_window(self):
        return self.acc_parent_count == 0

    @property
    def is_selected(self):
        result = False
        if self.acc_role_name == self._acc_role_name_map['AXRadioButton'] and \
                self._properties.get('AXValue', 'false') == 'true':
            result = True

        return result

    @property
    def is_checked(self):
        result = False
        if self.acc_role_name == self._acc_role_name_map['AXCheckBox'] and \
                self._properties.get('AXValue', 'false') == 'true':
            result = True

        return result

    @property
    def is_visible(self):
        return True  # We can't work with invisible elements under Mac OS.

    @property
    def is_enabled(self):
        return bool(self._properties.get('AXEnabled', False))

    @property
    def acc_parent_count(self):
        return self._layer_num

    @property
    def acc_child_count(self):
        children_elements = MacUtils.ApplescriptExecutor.get_children_elements(
            self._object_selector, self.acc_parent_count, self._proc_name)

        return len(children_elements[0])

    @property
    def acc_name(self):
        return self._properties.get('AXDescription', None)

    @property
    def set_focus(self):
        MacUtils.ApplescriptExecutor.set_element_attribute_value(
            self._object_selector, 'AXFocused', 'true', self._proc_name, False)

    @property
    def acc_c_name(self):
        return self.acc_role_name + self.acc_name if self.acc_name else ''

    @property
    def acc_location(self):
        x, y = self._properties['AXPosition']
        w, h = self._properties['AXSize']

        return map(int, [x, y, w, h])

    @property
    def acc_value(self):
        return self._properties.get('AXValue', None)

    @property
    def set_value(self, value):
        MacUtils.ApplescriptExecutor.set_element_attribute_value(
            self._object_selector, 'AXValue', value, self._proc_name)

    @property
    def acc_description(self):
        return self.acc_name

    @property
    def acc_parent(self):
        result = None
        event_descriptor = \
            MacUtils.ApplescriptExecutor.get_apple_event_descriptor(
                self._object_selector, self._proc_name)
        if self.acc_parent_count > 0 and event_descriptor.from_:
            result = \
                MacElement(event_descriptor.from_.applescript_specifier,
                           self.acc_parent_count - 1,
                           self._proc_name,
                           self.proc_id)

        return result

    @property
    def acc_selection(self):
        return self._properties.get('AXSelectedText', None)

    @property
    def acc_focused_element(self):
        childs = self.findall()

        result = None
        for element in childs:
            if self._properties.get('AXFocused', 'false') == 'true':
                result = element
                break

        return result

    @property
    def acc_role_name(self):
        return self._acc_role_name_map.get(self._role, 'unknown')

    def __iter__(self):
        children_elements = MacUtils.ApplescriptExecutor.get_children_elements(
            self._object_selector, self._layer_num, self._proc_name)

        children = children_elements[0]
        layer_number = children_elements[1]

        if not len(children):
            raise StopIteration()

        for el in children:
            yield MacElement(el, layer_number, self._proc_name, self.proc_id)

    def __findcacheiter(self, only_visible, **kwargs):
        """
        Find child element in the cache.

        Arguments:
            - only_visible: bool, flag that indicates will we search only

        Returns:
            - Yield found element.
        """

        for obj_element in self._cache:
            if obj_element._match(only_visible, **kwargs):
                yield obj_element

    def _finditer(self, only_visible, **kwargs):
        """
        Find child element.

        Arguments:
            - only_visible: bool, flag that indicates will we search only

        Returns:
            - Yield found element.
        """

        lst_queue = list(self)

        while lst_queue:
            obj_element = lst_queue.pop(0)
            self._cache.add(obj_element)

            if obj_element._match(only_visible, **kwargs):
                yield obj_element

            if self.acc_child_count:
                childs = [el for el in list(obj_element)]
                lst_queue[:0] = childs

    def find(self, only_visible=True, **kwargs):
        try:
            return self.__findcacheiter(only_visible,
                                        **kwargs).next()
        except StopIteration:
            try:
                return self._finditer(only_visible,
                                      **kwargs).next()
            except StopIteration:
                attrs = ['%s=%s' % (k, v) for k, v in kwargs.iteritems()]
                raise TooSaltyUISoupException(
                    'Can\'t find object with attributes "%s".' %
                    '; '.join(attrs))

    def findall(self, only_visible=True, **kwargs):
        result = self._finditer(only_visible, **kwargs)
        if result:
            result = list(result)

        return result

    def is_object_exists(self, **kwargs):
        try:
            self.find(**kwargs)
            return True
        except TooSaltyUISoupException:
            return False
