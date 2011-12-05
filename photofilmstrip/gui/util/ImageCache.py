# encoding: UTF-8
#
# PhotoFilmStrip - Creates movies out of your pictures.
#
# Copyright (C) 2011 Jens Goepfert
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import wx

from photofilmstrip.lib.common.Singleton import Singleton
from photofilmstrip.lib.common.ObserverPattern import Observer

from photofilmstrip.core import PILBackend


class ImageCache(Singleton, Observer):
    
    SIZE = 400
    THUMB_SIZE = 100
    
    def __init__(self):
        self._picRegistry = {}
        self._wxImgCache = {}
        self._wxBmpCache = {}
        self._pilCache = {}
        
    def ObservableUpdate(self, obj, arg):
        if arg == 'bitmap':
            self.UpdatePicture(obj)
                
    def ClearCache(self):
        self._wxImgCache.clear()
        self._wxBmpCache.clear()
    
    def RegisterPicture(self, picture, pilThumb=None):
        if pilThumb is None:
            pilThumb = PILBackend.GetThumbnail(picture, height=120)

        key = picture.GetKey()
        self._picRegistry[key] = picture
        self._pilCache[key] = pilThumb
        
        picture.AddObserver(self)
        
    def UpdatePicture(self, picture):
        key = picture.GetKey()
        if self._wxImgCache.has_key(key):
            del self._wxImgCache[key]
        if self._wxBmpCache.has_key(key):
            del self._wxBmpCache[key]
        if self._pilCache.has_key(key):
            del self._pilCache[key]
            
        self.RegisterPicture(picture)
    
    def GetImage(self, picture):
        key = picture.GetKey()
        if not self._wxImgCache.has_key(key):
            pilImg = PILBackend.GetThumbnail(picture, width=ImageCache.SIZE)
            wxImg = wx.ImageFromStream(PILBackend.ImageToStream(pilImg), wx.BITMAP_TYPE_JPEG)
            self._wxImgCache[key] = wxImg
        return self._wxImgCache[key]
    
    def GetThumbBmp(self, picture):
        key = picture.GetKey()
        if not self._wxBmpCache.has_key(key):
            if self._pilCache.has_key(key):
                pilImg = self._pilCache[key]
            else:
                pilImg = PILBackend.GetThumbnail(picture, height=ImageCache.THUMB_SIZE)
            wxImg = wx.ImageFromStream(PILBackend.ImageToStream(pilImg), wx.BITMAP_TYPE_JPEG)
            self._wxBmpCache[key] = wxImg.ConvertToBitmap()
        return self._wxBmpCache[key]
