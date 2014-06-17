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
from Foundation import NSAppleScript
from Carbon import AppleEvents

from ..utils import _Utils
from .. import TooSaltyUISoupException


class MacUtils(_Utils):

    @classmethod
    def execute_applescript_command(cls, cmd):
        """
        Executes command via osascript.

        Arguments:
            - cmd: string or list, command or commands that should be
            executed.

        Returns:
            - string with result of executed command.
        """

        cmd = '\n'.join([cmd] if isinstance(cmd, basestring) else cmd)

        script = NSAppleScript.alloc().initWithSource_(cmd)
        result = script.executeAndReturnError_(None)[0]

        if not result:
            raise TooSaltyUISoupException(
                'Error when executing applescript command.')

        return result

    class ApplescriptExecutor(object):

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
        def _parse_single_selector(cls, event_descriptor):
            """
            Parses single selector from NSAppleEventDescriptor.

            Arguments:
                - event_descriptor: NSAppleEventDescriptor, instance.

            Returns:
                - tuple with window name, process name.
            """

            seld_ = cls._get_aeKeyword(AppleEvents.keyAEKeyData)
            from_ = \
                cls._get_aeKeyword(AppleEvents.keyOriginalAddressAttr)
            window_name = \
                event_descriptor.descriptorForKeyword_(seld_).stringValue()
            process_name = event_descriptor.descriptorForKeyword_(from_)\
                .descriptorForKeyword_(seld_).stringValue()

            return window_name, process_name

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
            window_name, process_name = cls._parse_single_selector(event_descriptor)

            return window_name + process_name

        @classmethod
        def get_front_window_element(cls, process_name):
            """
            Gets front window element by given process name.

            Arguments:
                - process_name: string, name of process.

            Returns:
                - string with element selector.
            """

            cmd = ['tell application "System Events" to tell process "%s"'% process_name,
                   '  set visible to true',
                   '  return front window',
                   'end tell']

            event_descriptor = MacUtils.execute_applescript_command(cmd)
            window_name, process_name = \
                cls._parse_single_selector(event_descriptor)

            result = 'window "%s" of application process "%s" of ' \
                     'application "System Events"' % (window_name,
                                                      process_name)

            return result

        @classmethod
        def get_element_by_selector(cls, process_name, selector):
            """
            Gets element by given process name.

            Arguments:
                - process_name: string, name of process.
                - selector: string, selector of element.

            Returns:
                - List with Applescript commands.
            """

            return ['tell application "System Events" to tell process "%s"' % process_name,
                    '  set visible to true',
                    '  %s of application "System Events"' % selector,
                    'end tell']

        @classmethod
        def get_children_elements(cls, obj_selector, layer_num, process_name):
            """
            Gets all direct children elements.

            Arguments:
                - obj_selector: string, object selector.
                - layer_num: int, layer number. I.e. main window will be layer 0.
                - process_name: string, name of process.

            Returns:
                - List with Applescript commands.
            """

            return ['tell application "System Events" to tell process "%s"' % process_name,
                    '  set visible to true',
                    '  set uiElement to %s' % obj_selector,
                    '  set layer to %s' % layer_num,
                    '  if uiElement = null then',
                    '    set layer to 0',
                    '    set collectedElements to {UI elements of front window, layer}',
                    '  else',
                    '    set layer to layer + 1',
                    '    if name of attributes of uiElement contains "AXChildren" then',
                    '        set collectedElements to {value of attribute "AXChildren" of uiElement, layer}',
                    '    end if',
                    '  end if',
                    'end tell',
                    'return collectedElements']