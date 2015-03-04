# !/usr/bin/env python
# -*- coding: utf-8 -*-

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


import struct
from AppKit import NSAppleScript
from Carbon import AppleEvents

from ..utils import _Utils
from .. import TooSaltyUISoupException


class AppleEventDescriptor(object):

    @classmethod
    def _get_aeKeyword(cls, four_char_code):
        """
        Gets aeKeyword from four character event code.

        Arguments:
            - four_char_code: str, four character event code.

        Return:
            - integer aeKeyword.
        """

        return struct.unpack('>I', four_char_code)[0]

    @classmethod
    def _get_four_char_code(cls, ae_keyword):
        """
        Gets four char event code from aeKeyword.

        Arguments:
            - ae_keyword: integer, aeKeyword.

        Return:
            - string four char code.
        """

        return struct.pack('>I', ae_keyword)

    def __init__(self, event_descriptor):
        """
        Constructor.

        Arguments:
            - event_descriptor: NSAppleEventDescriptor, instance.
        """

        self._event_descriptor = event_descriptor

    def __iter__(self):
        """Iterate all nested elements"""

        if not self.class_name:
            i = 1
            while self._event_descriptor.descriptorAtIndex_(i):
                yield AppleEventDescriptor(
                    self._event_descriptor.descriptorAtIndex_(i))
                i += 1

        raise StopIteration()

    @property
    def form_(self):
        """
        Property for element "from" field.
        """

        from_ = self._event_descriptor.descriptorForKeyword_(
            self._get_aeKeyword(AppleEvents.keyAEKeyForm))

        result = AppleEventDescriptor(from_).string_value if from_ else None

        return result

    @property
    def class_name(self):
        """
        Property for element class name.
        """

        result = None

        if self._event_descriptor.typeCodeValue():
            ae_keyword = \
                self._event_descriptor.descriptorForKeyword_(
                    self._get_aeKeyword(
                        AppleEvents.keyAEDesiredClass))
            if ae_keyword:
                result = \
                    self._get_four_char_code(int(ae_keyword.typeCodeValue()))

        return result

    @property
    def class_id(self):
        """
        Property for element class id.
        """

        return (self.seld_.string_value or '').replace('\\', '\\\\')

    @property
    def seld_(self):
        """
        Property for "seld" field.
        """

        seld_ = self._event_descriptor.descriptorForKeyword_(
            self._get_aeKeyword(AppleEvents.keyAEKeyData))

        result = AppleEventDescriptor(seld_) if seld_ else None

        return result

    @property
    def from_(self):
        """
        Property for "from" field.
        """

        from_ = self._event_descriptor.descriptorForKeyword_(
            self._get_aeKeyword(AppleEvents.keyAEContainer))

        result = AppleEventDescriptor(from_) if from_ else None

        return result

    @property
    def string_value(self):
        """
        Property for string value.
        """

        return self._event_descriptor.stringValue()

    @property
    def applescript_specifier(self):
        """
        Property for applescript specifier.
        """

        if self.class_id:
            class_id = \
                self.class_id if self.form_ == AppleEvents.kFAIndexParam else \
                u'"%s"' % self.class_id.replace('"', '\\"')
            specifier = u'«class %s» %s' % (self.class_name, class_id)
        else:
            specifier = u'every «class %s»' % self.class_name

        if self.from_.class_name:
            # Sometimes applescript returns menu bar as a child of
            # window (cwin) but this is wrong and parent of menu bar should
            # be application (pcap) so we need to skip one parent (cwin) in
            # this case.
            parent_element = self.from_
            if self.class_name == 'mbar' and\
                    self.from_.class_name == AppleEvents.cWindow:
                parent_element = parent_element.from_
            specifier = '%s of %s' % (specifier,
                                      parent_element.applescript_specifier)
        else:
            specifier = '%s of application "System Events"' % specifier

        return specifier


class MacUtils(_Utils):

    @classmethod
    def execute_applescript_command(cls, cmd):
        """
        Executes applescript command.

        Arguments:
            - cmd: string or list, command or commands that should be
            executed.

        Returns:
            - AppleEventDescriptor with result of executed command.
        """

        cmd = '\n'.join([cmd] if isinstance(cmd, basestring) else cmd)

        script = NSAppleScript.alloc().initWithSource_(cmd)
        result = script.executeAndReturnError_(None)

        if not result[0]:
            error_message = 'Error when executing applescript command: %s' %\
                            result[1]['NSAppleScriptErrorMessage']
            raise TooSaltyUISoupException(error_message.encode('utf-8',
                                                               'ignore'))

        return AppleEventDescriptor(result[0])

    class ApplescriptExecutor(object):

        @classmethod
        def get_frontmost_window_name(cls):
            """
            Gets front window name.

            Arguments:
                - None

            Returns:
                - string with combined name (window name + process name).
            """

            cmd = ['tell application "System Events" to tell process (name of first application process whose frontmost is true)',
                   '  return (1st window whose value of attribute "AXMain" is true)',
                   'end tell']

            event_descriptor = MacUtils.execute_applescript_command(cmd)

            return event_descriptor.seld_.string_value + \
                event_descriptor.from_.seld_.string_value

        @classmethod
        def get_apple_event_descriptor(cls, obj_selector, process_name):
            """
            Gets apple event descriptor.

            Arguments:
                - obj_selector: string, object selector.
                - process_name: string, name of process.

            Returns:
                - instance of AppleEventDescriptor.
            """

            cmd = ['tell application "System Events" to tell process "%s"' % process_name,
                   '  set visible to true',
                   '  return %s' % obj_selector,
                   'end tell']

            return MacUtils.execute_applescript_command(cmd)

        @classmethod
        def get_children_elements(cls, obj_selector, layer_num, process_name):
            """
            Gets all direct children elements.

            Arguments:
                - obj_selector: string, object selector.
                - layer_num: int, layer number.
                I.e. main window will be layer 0.
                - process_name: string, name of process.

            Returns:
                - Tuple that contains dict of element selectors and
                elements layer number.
            """

            cmd = ['tell application "System Events" to tell process "%s"' % process_name,
                   '  set visible to true',
                   '  set uiElement to %s' % obj_selector,
                   '  set layer to %s' % layer_num,
                   '  if uiElement = null then',
                   '    set layer to 0',
                   '    set collectedElements to {UI elements of front window, layer}',
                   '  else',
                   '    set layer to layer + 1',
                   '    set collectedElements to {null, layer}',
                   '    if name of attributes of uiElement contains "AXChildren" then',
                   '        set collectedElements to {value of attribute "AXChildren" of uiElement, layer}',
                   '    end if',
                   '  end if',
                   'end tell',
                   'return collectedElements']

            event_descriptors_list = \
                list(MacUtils.execute_applescript_command(cmd))

            elements = [{'selector': el.applescript_specifier,
                         'class_id': el.class_id} for el in
                        list(event_descriptors_list[0])]

            return elements, int(event_descriptors_list[1].string_value)

        @classmethod
        def get_element_properties(cls, obj_selector, process_name):
            """
            Gets all element properties.

            Arguments:
                - obj_selector: string, object selector.
                - process_name: string, name of process.

            Returns:
                - Dict with element properties.
            """

            cmd = ['tell application "System Events" to tell application process "%s"' % process_name,
                   '  set visible to true',
                   '  set res to {}',
                   '  repeat with attr in attributes of %s' % obj_selector,
                   '    try',
                   '      set res to res & {{name of attr, value of attr}}',
                   '    end try',
                   '  end repeat',
                   '  return res',
                   'end tell']

            event_descriptors_list = list(
                MacUtils.execute_applescript_command(cmd))

            # Unpacking properties to dict.
            el_properties = dict()
            for prop in event_descriptors_list:
                prop = list(prop)
                prop_name = prop[0].string_value
                prop_value = [e.string_value for e in list(prop[1])] if \
                    list(prop[1]) else prop[1].string_value

                el_properties[prop_name] = prop_value

            return el_properties

        @classmethod
        def set_element_attribute_value(cls, obj_selector, attribute_name,
                                        value, process_name,
                                        string_value=True):
            """
            Sets element attribute.

            Arguments:
                - obj_selector: string, object selector.
                - attribute_name: string, name of attribute:
                - value: string, value.
                - process_name: string, name of process.
                - string_value: bool, indicates will be value wrapped in
                brackets.

            Returns:
                - Boolean indicator whether was operation successful or not.
            """

            value = '"%s"' % value if string_value else value
            cmd = ['tell application "System Events" to tell application process "%s"' % process_name,
                   '  set value of attribute "%s" of %s to %s' % (attribute_name, obj_selector, value),
                   'end tell']

            try:
                MacUtils.execute_applescript_command(cmd)
                result = True
            except TooSaltyUISoupException:
                result = False

            return result

        @classmethod
        def get_axunknown_windows(cls, process_name):
            """
            Gets AXUnknown windows by given process name.

            Arguments:
                - process_name: string, name of process.

            Returns:
                - List of AppleEventDescriptor elements.
            """

            cmd = ['tell application "System Events" to tell process "%s"' % process_name,
                   '  set visible to true',
                   '  set unknownWindows to {}',
                   '  repeat with e in UI elements',
                   '    if value of attribute "AXRole" of e is equal to "AXUnknown" then',
                   '      set unknownWindows to unknownWindows & {e}',
                   '    end if',
                   '  end repeat',
                   '  return unknownWindows',
                   'end tell']

            return list(MacUtils.execute_applescript_command(cmd))

        @classmethod
        def get_axdialog_windows(cls, process_name):
            """
            Gets AXDialog windows by given process name.

            Arguments:
                - process_name: string, name of process.

            Returns:
                - List of AppleEventDescriptor elements.
            """

            cmd = ['tell application "System Events" to tell process "%s"' % process_name,
                   '  set visible to true',
                   '  set dialogWindows to {}',
                   '  repeat with e in UI elements',
                   '    if value of attribute "AXRole" of e is equal to "AXWindow" and value of attribute "AXSubrole" of e is equal to "AXDialog" then',
                   '      set dialogWindows to dialogWindows & {e}',
                   '    end if',
                   '  end repeat',
                   '  return dialogWindows',
                   'end tell']

            return list(MacUtils.execute_applescript_command(cmd))
