# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2015 Michal Čihař <michal@cihar.com>
# Copyright © 2015 Philipp Wolfer <ph.wolfer@gmail.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Tests for AngularJS checks.
"""

from unittest import TestCase
from weblate.trans.checks.angularjs import AngularJSInterpolationCheck
from weblate.trans.tests.test_checks import MockUnit


class AngularJSInterpolationCheckTest(TestCase):
    def setUp(self):
        self.check = AngularJSInterpolationCheck()

    def test_no_format(self):
        self.assertFalse(self.check.check_single(
            'strins',
            'string',
            MockUnit('angularjs_no_format'),
            0
        ))

    def test_format(self):
        self.assertFalse(self.check.check_single(
            u'{{name}} string {{other}}',
            u'{{name}} {{other}} string',
            MockUnit('angularjs_format'),
            0
        ))

    def test_format_ignore_position(self):
        self.assertFalse(self.check.check_single(
            u'{{name}} string {{other}}',
            u'{{other}} string {{name}}',
            MockUnit('angularjs_format_ignore_position'),
            0
        ))

    def test_different_whitespace(self):
        self.assertFalse(self.check.check_single(
            u'{{ name   }} string',
            u'{{name}} string',
            MockUnit('angularjs_different_whitespace'),
            0
        ))

    def test_missing_format(self):
        self.assertTrue(self.check.check_single(
            u'{{name}} string',
            u'string',
            MockUnit('angularjs_missing_format'),
            0
        ))

    def test_wrong_value(self):
        self.assertTrue(self.check.check_single(
            u'{{name}} string',
            u'{{notname}} string',
            MockUnit('angularjs_wrong_value'),
            0
        ))
