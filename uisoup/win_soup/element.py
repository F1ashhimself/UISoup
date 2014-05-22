#!/usr/bin/env python

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

import re
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.automation
import comtypes.client
from inspect import ismethod
from types import FunctionType
import xml.dom.minidom

from .mouse import WinMouse
from ..interfaces.i_element import IElement
from .. import TooSaltyUISoupException


CO_E_OBJNOTCONNECTED = -2147220995


class WinElement(IElement):
    """
    http://msdn.microsoft.com/en-us/library/dd318466(v=VS.85).aspx
    """

    _acc_role_name_map = {
        1: u'ttl',  # TitleBar
        2: u'mnu',  # MenuBar
        3: u'scbr',  # ScrollBar
        4: u'grip',  # Grip
        5: u'snd',  # Sound
        6: u'cur',  # Cursor
        7: u'caret',  # Caret
        8: u'alrt',  # Alert
        9: u'frm',  # Window
        10: u'clnt',  # Client
        11: u'mnu',  # PopupMenu
        12: u'mnu',  # MenuItem
        13: u'ttip',  # Tooltip
        14: u'app',  # Application
        15: u'doc',  # Document
        16: u'pane',  # Pane
        17: u'chrt',  # Chart
        18: u'dlg',  # Dialog
        19: u'border',  # Border
        20: u'grp',  # Grouping
        21: u'sep',  # Separator
        22: u'tbar',  # ToolBar
        23: u'sbar',  # StatusBar
        24: u'tbl',  # Table
        25: u'chdr',  # ColumnHeader
        26: u'rhdr',  # RowHeader
        27: u'col',  # Column
        28: u'tblc',  # Row
        29: u'tblc',  # Cell
        30: u'lnk',  # Link
        31: u'hbal',  # HelpBalloon
        32: u'chr',  # Character
        33: u'lst',  # List
        34: u'lst',  # ListItem
        35: u'otl',  # Outline
        36: u'otl',  # OutlineItem
        37: u'ptab',  # PageTab
        38: u'ppage',  # PropertyPage
        39: u'val',  # Indicator
        40: u'grph',  # Graphic
        41: u'lbl',  # Text
        42: u'txt',  # EditableText
        43: u'btn',  # PushButton
        44: u'chk',  # CheckBox
        45: u'rbtn',  # RadioButton
        46: u'cbox',  # ComboBox
        47: u'ddwn',  # DropDown
        48: u'pbar',  # ProgressBar
        49: u'dial',  # Dial
        50: u'hkfield',  # HotKeyField
        51: u'sldr',  # Slider
        52: u'sbox',  # SpinBox
        53: u'dgrm',  # Diagram
        54: u'anim',  # Animation
        55: u'eqtn',  # Equation
        56: u'btn',  # DropDownButton
        57: u'mnu',  # MenuButton
        58: u'gbtn',  # GridDropDownButton
        59: u'wspace',  # WhiteSpace
        60: u'ptablst',  # PageTabList
        61: u'clock',  # Clock
        62: u'sbtn',  # SplitButton
        63: u'ip',  # IPAddress
        64: u'obtn'  # OutlineButton
    }

    _mouse = WinMouse()

    class StateFlag(object):
        SYSTEM_NORMAL = 0
        SYSTEM_UNAVAILABLE = 0x1
        SYSTEM_SELECTED = 0x2
        SYSTEM_FOCUSED = 0x4
        SYSTEM_PRESSED = 0x8
        SYSTEM_CHECKED = 0x10
        SYSTEM_MIXED = 0x20
        SYSTEM_READONLY = 0x40
        SYSTEM_HOTTRACKED = 0x80
        SYSTEM_DEFAULT = 0x100
        SYSTEM_EXPANDED = 0x200
        SYSTEM_COLLAPSED = 0x400
        SYSTEM_BUSY = 0x800
        SYSTEM_FLOATING = 0x1000
        SYSTEM_MARQUEED = 0x2000
        SYSTEM_ANIMATED = 0x4000
        SYSTEM_INVISIBLE = 0x8000
        SYSTEM_OFFSCREEN = 0x10000
        SYSTEM_SIZEABLE = 0x20000
        SYSTEM_MOVEABLE = 0x40000
        SYSTEM_SELFVOICING = 0x80000
        SYSTEM_FOCUSABLE = 0x100000
        SYSTEM_SELECTABLE = 0x200000
        SYSTEM_LINKED = 0x400000
        SYSTEM_TRAVERSED = 0x800000
        SYSTEM_MULTISELECTABLE = 0x1000000
        SYSTEM_EXTSELECTABLE = 0x2000000
        SYSTEM_ALERT_LOW = 0x4000000
        SYSTEM_ALERT_MEDIUM = 0x8000000
        SYSTEM_ALERT_HIGH = 0x10000000
        SYSTEM_PROTECTED = 0x20000000
        SYSTEM_HASPOPUP = 0x40000000
        SYSTEM_VALID = 0x7fffffff

    class SelectionFlag(object):
        NONE = 0
        TAKEFOCUS = 0x1
        TAKESELECTION = 0x2
        EXTENDSELECTION = 0x4
        ADDSELECTION = 0x8
        REMOVESELECTION = 0x10
        VALID = 0x20

    class _EnumWindowsCallback(object):

        same_proc_handles = set()

        @classmethod
        def callback(cls, handle, proc_id):

            curr_proc_id = ctypes.c_long()

            ctypes.windll.user32.GetWindowThreadProcessId(
                handle, ctypes.byref(curr_proc_id))

            if curr_proc_id.value == proc_id:
                cls.same_proc_handles.add(handle)

            return True

    def __init__(self, obj_handle, i_object_id):
        if isinstance(obj_handle, comtypes.gen.Accessibility.IAccessible):
            i_accessible = obj_handle
        else:
            i_accessible = ctypes.POINTER(
                comtypes.gen.Accessibility.IAccessible)()
            ctypes.oledll.oleacc.AccessibleObjectFromWindow(
                obj_handle,
                0,
                ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
                ctypes.byref(i_accessible))

        self._i_accessible = i_accessible
        self.i_object_id = i_object_id
        self._cache = set()

    def click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.click(x, y)

    def right_click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.click(x, y, self._mouse.RIGHT_BUTTON)

    def double_click(self, x_offset=0, y_offset=0):
        x, y, w, h = self.acc_location
        x += x_offset if x_offset is not None else w / 2
        y += y_offset if y_offset is not None else h / 2

        self._mouse.double_click(x, y)

    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        el_x, el_y, el_w, el_h = self.acc_location
        el_x += x_offset if x_offset is not None else el_w / 2
        el_y += y_offset if y_offset is not None else el_h / 2

        self._mouse.drag(el_x, el_y, x, y, smooth)

    def check_state(self, state):
        return bool(self.acc_state & state)

    def _find_windows_by_same_proc(self):
        """
        Find window by same process id.

        Arguments:
            - None

        Returns:
            - list of windows.
        """

        enum_windows_proc = \
            ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_long,
                               ctypes.c_long)
        self._EnumWindowsCallback.same_proc_handles = set()
        ctypes.windll.user32.EnumWindows(
            enum_windows_proc(
                self._EnumWindowsCallback.callback), self.proc_id)

        if self.hwnd in self._EnumWindowsCallback.same_proc_handles:
            self._EnumWindowsCallback.same_proc_handles.remove(self.hwnd)

        result = [WinElement(hwnd, 0) for hwnd in
                  self._EnumWindowsCallback.same_proc_handles]

        return result

    @property
    def hwnd(self):
        hwnd = ctypes.c_int()
        ctypes.oledll.oleacc.WindowFromAccessibleObject(self._i_accessible,
                                                        ctypes.byref(hwnd))

        return hwnd.value

    @property
    def proc_id(self):
        hwnd = ctypes.c_long(self.hwnd)
        proc_id = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd,
                                                      ctypes.byref(proc_id))

        return proc_id.value

    @property
    def is_top_level_window(self):
        # Top level window have 2 parents, clnt and frm for Desktop.
        return self.acc_parent_count == 2

    @property
    def is_selected(self):
        return self.check_state(self.StateFlag.SYSTEM_SELECTED)

    @property
    def is_pressed(self):
        return self.check_state(self.StateFlag.SYSTEM_PRESSED)

    @property
    def is_checked(self):
        return self.check_state(self.StateFlag.SYSTEM_CHECKED)

    @property
    def is_visible(self):
        return not self.check_state(self.StateFlag.SYSTEM_INVISIBLE)

    @property
    def is_enabled(self):
        return not self.check_state(self.StateFlag.SYSTEM_UNAVAILABLE)

    @property
    def acc_parent_count(self):
        parent_count = 0
        parent = self.acc_parent
        while parent:
            parent_count += 1
            parent = parent.acc_parent

        return parent_count

    @property
    def acc_child_count(self):
        if self.i_object_id == 0:
            return self._i_accessible.accChildCount
        else:
            return 0

    @property
    def acc_role(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_role = comtypes.automation.VARIANT()
        obj_role.vt = comtypes.automation.VT_BSTR

        self._i_accessible._IAccessible__com__get_accRole(obj_child_id,
                                                          obj_role)

        return obj_role.value

    @property
    def acc_name(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id

        obj_name = comtypes.automation.BSTR()

        self._i_accessible._IAccessible__com__get_accName(
            obj_child_id, ctypes.byref(obj_name))

        return obj_name.value

    def set_name(self, name):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id

        self._i_accessible._IAccessible__com__set_accName(obj_child_id, name)

    def set_focus(self):
        self.acc_select(self.SelectionFlag.TAKEFOCUS)

    @property
    def acc_c_name(self):
        return self.acc_role_name + self.acc_name if self.acc_name else ''

    @property
    def acc_location(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id

        obj_l, obj_t, obj_w, obj_h = ctypes.c_long(), ctypes.c_long(), \
            ctypes.c_long(), ctypes.c_long()

        self._i_accessible._IAccessible__com_accLocation(ctypes.byref(obj_l),
                                                         ctypes.byref(obj_t),
                                                         ctypes.byref(obj_w),
                                                         ctypes.byref(obj_h),
                                                         obj_child_id)

        return obj_l.value, obj_t.value, obj_w.value, obj_h.value

    @property
    def acc_value(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_bstr_value = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accValue(
            obj_child_id, ctypes.byref(obj_bstr_value))

        return obj_bstr_value.value

    def set_value(self, value):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id

        self._i_accessible._IAccessible__com__set_accValue(obj_child_id, value)

    @property
    def acc_default_action(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_default_action = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accDefaultAction(
            obj_child_id, ctypes.byref(obj_default_action))

        return obj_default_action.value

    @property
    def acc_description(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_description = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accDescription(
            obj_child_id, ctypes.byref(obj_description))

        return obj_description.value

    @property
    def acc_help(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_help = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_accHelp(
            obj_child_id, ctypes.byref(obj_help))

        return obj_help.value

    @property
    def acc_help_topic(self):
        return self._i_accessible.acc_help_topic()

    @property
    def acc_keyboard_shortcut(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_keyboard_shortcut = comtypes.automation.BSTR()
        self._i_accessible._IAccessible__com__get_acccKeyboardShortcut(
            obj_child_id, ctypes.byref(obj_keyboard_shortcut))

        return obj_keyboard_shortcut.value

    @property
    def acc_parent(self):
        result = None
        if self._i_accessible.accParent:
            result = WinElement(self._i_accessible.accParent, self.i_object_id)

        return result

    @property
    def acc_selection(self):
        obj_children = comtypes.automation.VARIANT()
        self._i_accessible._IAccessible__com__get_accSelection(
            ctypes.byref(obj_children))

        return obj_children.value

    @property
    def acc_state(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id
        obj_state = comtypes.automation.VARIANT()
        self._i_accessible._IAccessible__com__get_accState(
            obj_child_id, ctypes.byref(obj_state))

        return obj_state.value

    def acc_do_default_action(self):
        obj_child_id = comtypes.automation.VARIANT()
        obj_child_id.vt = comtypes.automation.VT_I4
        obj_child_id.value = self.i_object_id

        self._i_accessible._IAccessible__com_accDoDefaultAction(obj_child_id)

    @property
    def acc_focus(self):
        result = None
        if self._i_accessible.accFocus:
            result = WinElement(self._i_accessible.accFocus, self.i_object_id)

        return result

    def acc_select(self, i_selection):
        if self.i_object_id:
            return self._i_accessible.accSelect(i_selection, self.i_object_id)
        else:
            return self._i_accessible.accSelect(i_selection)

    @property
    def acc_role_name(self):
        return self._acc_role_name_map.get(self.acc_role, 'unknown')

    def __iter__(self):
        if self.i_object_id > 0:
            raise StopIteration()

        obj_acc_child_array = (comtypes.automation.VARIANT *
                               self._i_accessible.accChildCount)()
        obj_acc_child_count = ctypes.c_long()

        ctypes.oledll.oleacc.AccessibleChildren(
            self._i_accessible,
            0,
            self._i_accessible.accChildCount,
            obj_acc_child_array,
            ctypes.byref(obj_acc_child_count))

        for i in xrange(obj_acc_child_count.value):
            obj_acc_child = obj_acc_child_array[i]
            if obj_acc_child.vt == comtypes.automation.VT_DISPATCH:
                yield WinElement(obj_acc_child.value.QueryInterface(
                    comtypes.gen.Accessibility.IAccessible), 0)
            else:
                yield WinElement(self._i_accessible, obj_acc_child.value)

    def __str__(self):
        result = '[Role: %s(0x%X) | Name: %r | Child count: %d]' % \
                 (self._acc_role_name_map.get(self.acc_role, 'Unknown'),
                  self.acc_role,
                  self.acc_name,
                  self._i_accessible.accChildCount)

        return result

    @classmethod
    def _convert_wildcard_to_regex(cls, wildcard):
        """
        Converts wildcard to regex.

        Arguments:
            - wildcard: string, wildcard.

        Returns:
            - String with regex pattern.
        """

        regex = re.escape(wildcard)
        regex = regex.replace(r'\?', r'[\s\S]{1}')
        regex = regex.replace(r'\*', r'[\s\S]*')

        return '^%s$' % regex

    def _match(self, only_visible, **kwargs):
        """
        Match method.

        Arguments:
            - only_visible: bool, flag that indicates will we search only
            through visible elements.
            - role: string or lambda e.g. lambda x: x == 13
            - name: string or lambda.
            - c_name: string or lambda.
            - location: string or lambda.
            - value: string or lambda.
            - default_action: string or lambda.
            - description: string or lambda.
            - help: string or lambda.
            - help_topic: string or lambda.
            - keyboard_shortcut: string or lambda.
            - parent: string or lambda.
            - selection: string or lambda.
            - state: string or lambda.
            - focus: string or lambda.
            - role_name: string or lambda.

        Returns:
            - True if element was matched otherwise False.
        """

        try:
            if only_visible and not self.is_visible:
                return False

            for str_property in kwargs:
                attr = getattr(self, 'acc_' + str_property)
                if ismethod(attr):
                    attr = attr()

                expected_result = kwargs[str_property]
                if type(expected_result) is FunctionType:
                    if not expected_result(attr):
                        return False
                else:
                    regex = self._convert_wildcard_to_regex(expected_result)
                    if not re.match(regex, attr):
                        return False
        except:
            return False
        else:
            return True

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

        if self.is_top_level_window:
            lst_queue.extend(self._find_windows_by_same_proc())

        while lst_queue:
            obj_element = lst_queue.pop(0)
            self._cache.add(obj_element)

            if obj_element._match(only_visible, **kwargs):
                yield obj_element

            if self._get_child_count_safely(obj_element._i_accessible):
                childs = [el for el in list(obj_element) if
                          el._i_accessible != obj_element._i_accessible]

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

    def toxml(self):
        obj_document = xml.dom.minidom.Document()
        lst_queue = [(self, obj_document)]

        while lst_queue:
            obj_element, obj_tree = lst_queue.pop(0)
            role_name = obj_element.acc_role_name
            obj_name = obj_element.acc_name
            str_name = unicode(obj_name) if obj_name else ''
            str_location = ','.join(str(x) for x in obj_element.acc_location)
            obj_sub_tree = xml.dom.minidom.Element(role_name)
            obj_sub_tree.ownerDocument = obj_document

            try:
                obj_sub_tree.attributes['Name'] = str_name
            except:
                obj_sub_tree.attributes['Name'] = \
                    str_name.encode('unicode-escape')

            obj_sub_tree.attributes['Location'] = str_location
            obj_tree.appendChild(obj_sub_tree)

            if self._get_child_count_safely(obj_element._i_accessible):
                for obj_element_child in obj_element:
                    lst_queue.append((obj_element_child, obj_sub_tree))

        return obj_document.toprettyxml()

    def _get_child_count_safely(self, i_accessible):
        """
        Safely gets child count.

        Arguments:
            - i_accessible: instance of i_accessible.

        Returns:
            - int, object child count.
        """

        try:
            return i_accessible.accChildCount
        except Exception as ex:
            if isinstance(ex, comtypes.COMError) and ex.hresult in \
                    (CO_E_OBJNOTCONNECTED,):
                return 0
