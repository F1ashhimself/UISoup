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


from subprocess import check_output

from ..utils import _Utils


class ApplescriptCommands(object):

    @classmethod
    def get_front_window_element(cls, process_name):
        """
        Gets front window element by given process name.

        Arguments:
            - process_name: string, name of process.

        Returns:
            - List with Applescript commands.
        """

        return ['tell application "System Events" to tell process "%s"' % process_name,
                '  set visible to true',
                '  return front window',
                'end tell']

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
    def collect_all_window_elements(cls, process_name):
        """
        Collects all window elements by given process name.

        Arguments:
            - process_name: string, name of process.

        Returns:
            - List with Applescript commands.
        """

        return ['on buildElementsTree(uiElements)',
                '  tell application "System Events" to tell process "%s"' % process_name,
                '    set visible to true',
                '    if uiElements = null then',
                '      set uiElements to UI elements of front window',
                '    end if',
                '    set collectedElements to uiElements',
                '    repeat with uiElement in collectedElements',
                '      if name of attributes of uiElement contains "AXChildren" then',
                '        set collectedElements to collectedElements & my buildElementsTree(value of attribute "AXChildren" of uiElement)',
                '      end if',
                '    end repeat',
                '  end tell',
                '  return collectedElements',
                'end buildElementsTree',
                'return my buildElementsTree(null)']


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

        cmd_pattern = "-e '%s'"
        cmd = [cmd] if isinstance(cmd, basestring) else cmd
        full_cmd = \
            ' '.join(['osascript'] + [cmd_pattern % c.strip() for c in cmd])

        return check_output(full_cmd, shell=True)
