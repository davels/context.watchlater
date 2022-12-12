# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 davels
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

import sys
import xbmc
import xbmcgui
import xbmcaddon
import json


JSON_ID = 'watchlater'
__settings = xbmcaddon.Addon()
__language = __settings.getLocalizedString


def _s(id):
    return str(__language(id))


def main():
    watch_tagname = __settings.getSetting("tagname")
    videoinfo = sys.listitem.getVideoInfoTag()
    videoid = videoinfo.getDbId()
    videotype = videoinfo.getMediaType()

    # get current tags on item
    gettags_json = {'jsonrpc': '2.0', 'id': JSON_ID,
                    'method': 'VideoLibrary.Get' + videotype + 'Details',
                    'params': {videotype + 'id': videoid,
                               'properties': ['tag']}}
    resp = json.loads(xbmc.executeJSONRPC(json.dumps(gettags_json)))
    tags = resp['result'][videotype + 'details']['tag']

    messageid=0
    if watch_tagname in tags:
        tags.remove(watch_tagname)
        messageid = 32005
    else:
        tags.append(watch_tagname)
        messageid = 32004

    # set tags on item
    settags_json = {'jsonrpc': '2.0', 'id': JSON_ID,
                    'method': 'VideoLibrary.Set' + videotype + 'Details',
                    'params': {videotype + 'id': videoid,
                               'tag': tags}}
    xbmc.executeJSONRPC(json.dumps(settags_json))
    message = '{0} {1}'.format(_s(messageid), watch_tagname)
    xbmcgui.Dialog().notification(sys.listitem.getLabel(), message)



if __name__ == '__main__':
    main()
