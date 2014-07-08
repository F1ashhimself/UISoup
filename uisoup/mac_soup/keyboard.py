#!/usr/bin/env python
#
#    Copyright (c) 2014 Oleksandr Iakovenko.
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

__author__ = 'alex.jakovenko@gmail.com'

from Quartz import CoreGraphics as CG

from time import sleep

from ..interfaces.i_keyboard import Key, IKeyboard


class MacKeyboard(IKeyboard):

    class _KeyCodes(object):
        """ Holder for Macintosh keyboard codes stored as Keys.
        """

        LEFT_ALT = Key(0x3A)  # Left ALT key
        RIGHT_ALT = Key(0x3D)  # Right ALT key
        LEFT_SHIFT = Key(0x38)  # Left SHIFT key
        RIGHT_SHIFT = Key(0x3C)  # Right SHIFT key
        LEFT_CONTROL = Key(0x3B)  # Left CONTROL key
        RIGHT_CONTROL = Key(0x3E)  # Right CONTROL key
        LEFT_COMMAND = Key(0x37)  # Left COMMAND key
        RIGHT_COMMAND = Key(0x36)  # Right COMMAND key
        BACKSPACE = Key(0x33)  # BACKSPACE key
        TAB = Key(0x30)  # TAB key
        CLEAR = Key(0x47)  # CLEAR key
        RETURN = Key(0x24)  # ENTER key
        SHIFT = LEFT_SHIFT  # SHIFT key
        CONTROL = LEFT_CONTROL  # CTRL key
        ALT = LEFT_ALT  # ALT key
        CAPS_LOCK = Key(0x39)  # CAPS LOCK key
        ESCAPE = Key(0x35)  # ESC key
        SPACE = Key(0x31)  # SPACEBAR
        PAGE_UP = Key(0x74)  # PAGE UP key
        PAGE_DOWN = Key(0x79)  # PAGE DOWN key
        END = Key(0x77)  # END key
        HOME = Key(0x73)  # HOME key
        LEFT = Key(0x7B)  # LEFT ARROW key
        UP = Key(0x7E)  # UP ARROW key
        RIGHT = Key(0x7C)  # RIGHT ARROW key
        DOWN = Key(0x7D)  # DOWN ARROW key
        INSERT = Key(0x72)  # INS key
        DELETE = Key(0x75)  # DEL key
        KEY_0 = Key(0x1D)  # 0 key
        KEY_1 = Key(0x12)  # 1 key
        KEY_2 = Key(0x13)  # 2 key
        KEY_3 = Key(0x14)  # 3 key
        KEY_4 = Key(0x15)  # 4 key
        KEY_5 = Key(0x17)  # 5 key
        KEY_6 = Key(0x16)  # 6 key
        KEY_7 = Key(0x1A)  # 7 key
        KEY_8 = Key(0x1C)  # 8 key
        KEY_9 = Key(0x19)  # 9 key
        KEY_A = Key(0x00)  # A key
        KEY_B = Key(0x0B)  # B key
        KEY_C = Key(0x08)  # C key
        KEY_D = Key(0x02)  # D key
        KEY_E = Key(0x0E)  # E key
        KEY_F = Key(0x03)  # F key
        KEY_G = Key(0x05)  # G key
        KEY_H = Key(0x04)  # H key
        KEY_I = Key(0x22)  # I key
        KEY_J = Key(0x26)  # J key
        KEY_K = Key(0x28)  # K key
        KEY_L = Key(0x25)  # L key
        KEY_M = Key(0x2E)  # M key
        KEY_N = Key(0x2D)  # N key
        KEY_O = Key(0x1F)  # O key
        KEY_P = Key(0x23)  # P key
        KEY_Q = Key(0x0C)  # Q key
        KEY_R = Key(0x0F)  # R key
        KEY_S = Key(0x01)  # S key
        KEY_T = Key(0x11)  # T key
        KEY_U = Key(0x20)  # U key
        KEY_V = Key(0x09)  # V key
        KEY_W = Key(0x0D)  # W key
        KEY_X = Key(0x07)  # X key
        KEY_Y = Key(0x10)  # Y key
        KEY_Z = Key(0x06)  # Z key
        NUMPAD0 = Key(0x52)  # Numeric keypad 0 key
        NUMPAD1 = Key(0x53)  # Numeric keypad 1 key
        NUMPAD2 = Key(0x54)  # Numeric keypad 2 key
        NUMPAD3 = Key(0x55)  # Numeric keypad 3 key
        NUMPAD4 = Key(0x56)  # Numeric keypad 4 key
        NUMPAD5 = Key(0x57)  # Numeric keypad 5 key
        NUMPAD6 = Key(0x58)  # Numeric keypad 6 key
        NUMPAD7 = Key(0x59)  # Numeric keypad 7 key
        NUMPAD8 = Key(0x5B)  # Numeric keypad 8 key
        NUMPAD9 = Key(0x5C)  # Numeric keypad 9 key
        MULTIPLY = Key(0x43)  # Multiply key
        ADD = Key(0x45)  # Add key
        SUBTRACT = Key(0x4E)  # Subtract key
        DECIMAL = Key(0x41)  # Decimal key
        DIVIDE = Key(0x4B)  # Divide key
        F1 = Key(0x7A)  # F1 key
        F2 = Key(0x78)  # F2 key
        F3 = Key(0x63)  # F3 key
        F4 = Key(0x76)  # F4 key
        F5 = Key(0x60)  # F5 key
        F6 = Key(0x61)  # F6 key
        F7 = Key(0x62)  # F7 key
        F8 = Key(0x64)  # F8 key
        F9 = Key(0x65)  # F9 key
        F10 = Key(0x6D)  # F10 key
        F11 = Key(0x67)  # F11 key
        F12 = Key(0x6F)  # F12 key
        OEM_1 = Key(0x29)  # For the US standard keyboard, the ';:' key
        OEM_PLUS = Key(0x18)  # For any country/region, the '+' key
        OEM_COMMA = Key(0x2B)  # For any country/region, the ',' key
        OEM_MINUS = Key(0x1B)  # For any country/region, the '-' key
        OEM_PERIOD = Key(0x2F)  # For any country/region, the '.' key
        OEM_2 = Key(0x2C)  # For the US standard keyboard, the '/?' key
        OEM_3 = Key(0x32)  # For the US standard keyboard, the '`~' key
        OEM_4 = Key(0x21)  # For the US standard keyboard, the '[{' key
        OEM_5 = Key(0x2A)  # For the US standard keyboard, the '\|' key
        OEM_6 = Key(0x1E)  # For the US standard keyboard, the ']}' key
        OEM_7 = Key(0x27)  # For the US standard keyboard, the ''"' key

    codes = _KeyCodes

    def press_key(self, hex_key_code):
        """Presses (and releases) key specified by a hex code.

        Arguments:
            - hex_key_code: integer value holding hexadecimal code for a key to
            be pressed.
        Returns:
            - None
        """

        self.press_key_and_hold(hex_key_code)
        self.release_key(hex_key_code)

    def press_key_and_hold(self, hex_key_code):
        """Presses (and holds) key specified by a hex code.

        Arguments:
            - hex_key_code: integer value holding hexadecimal code for a key to
            be pressed.
        Returns:
            - None
        """

        CG.CGEventPost(
            CG.kCGHIDEventTap,
            CG.CGEventCreateKeyboardEvent(None, hex_key_code, True))

    def release_key(self, hex_key_code):
        """Releases key specified by a hex code.

        Arguments:
            - hex_key_code: integer value holding hexadecimal code for a key to
            be pressed.
        Returns:
            - None
        """

        CG.CGEventPost(
            CG.kCGHIDEventTap,
            CG.CGEventCreateKeyboardEvent(None, hex_key_code, False))

    def send(self, *args):
        """Send key events as specified by Keys.

        If Key contains children Keys they will be recursively
        processed with current Key code pressed as a modifier key.

        Arguments:
            - *args: Keys to be send.
        Returns:
            - None
        """

        for key in args:
            if key.children:
                self.press_key_and_hold(key.code)
                self._wait_for_key_combo_to_be_processed()
                self.send(*key.children)
                self.release_key(key.code)
            else:
                self.press_key(key.code)
            self._wait_for_key_combo_to_be_processed()

    def _wait_for_key_combo_to_be_processed(self):
        # For key combinations timeout is needed to be processed.
        # This method is expressive shortcut to be used where needed.
        sleep(.05)
