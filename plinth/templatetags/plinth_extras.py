#
# This file is part of Plinth.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
from django import template

register = template.Library()


def mark_active_menuitem(menu, path):
    """Mark the best-matching menu item with 'active'

    Input: a menu dict in the form of:
    {'title': 'x',
     'items': [{'url': 'a/b', 'text': 'myUrl'}, {'url': ...}]
    }

    Output: The same dictionary; the best-matching URL dict gets the value
    'active': True. All other URL dicts get the value 'active': False.

    Note: this sets the 'active' values on the menu itself, not on a copy.
    """
    best_match = ''
    best_match_item = None

    for urlitem in menu['items']:
        urlitem['active'] = False
        # TODO: use a more suitable function instead of os.path.commonprefix
        match = os.path.commonprefix([urlitem['url'], path])
        # In case of 'xx/create' and 'xx/change' we'd have 'xx/c' as prefix.
        # That's a wrong match, skip it.
        match_clean = match.rpartition('/')[0]
        if (len(match_clean) + 1) < len(match):
            continue

        if len(match_clean) > len(best_match):
            best_match = match
            best_match_item = urlitem

    if best_match_item:
        best_match_item['active'] = True

    return menu


@register.inclusion_tag('subsubmenu.html', takes_context=True)
def show_subsubmenu(context, menudata):
    """Mark the active menu item and display the subsubmenu"""
    menudata = mark_active_menuitem(menudata, context['request'].path)
    return {'subsubmenu': menudata}