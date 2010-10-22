#Boa:Dialog:DlgRendererProps
# encoding: UTF-8
#
# PhotoFilmStrip - Creates movies out of your pictures.
#
# Copyright (C) 2010 Jens Goepfert
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

from lib.Settings import Settings
from lib.util import Encode

from gui.HelpViewer import HelpViewer


[wxID_DLGRENDERERPROPS, wxID_DLGRENDERERPROPSBMPHDR, 
 wxID_DLGRENDERERPROPSCMDCANCEL, wxID_DLGRENDERERPROPSCMDHELP, 
 wxID_DLGRENDERERPROPSCMDOK, wxID_DLGRENDERERPROPSLCPROPS, 
 wxID_DLGRENDERERPROPSPNLHDR, wxID_DLGRENDERERPROPSSLHDR, 
 wxID_DLGRENDERERPROPSSTATICLINE, wxID_DLGRENDERERPROPSSTHDR, 
] = [wx.NewId() for _init_ctrls in range(10)]


class DlgRendererProps(wx.Dialog):
    
    _custom_classes = {"wx.Choice": ["FormatComboBox"]}
    
    def _init_coll_sizerCmd_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.cmdHelp, 0, border=0, flag=0)
        parent.AddStretchSpacer(1)
        parent.AddWindow(self.cmdCancel, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.cmdOk, 0, border=0, flag=0)

    def _init_coll_szHdr_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.bmpHdr, 0, border=8, flag=wx.ALL)
        parent.AddWindow(self.stHdr, 0, border=8,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

    def _init_coll_sizerMain_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.pnlHdr, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.slHdr, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.lcProps, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.staticLine, 0, border=8,
              flag=wx.TOP | wx.BOTTOM | wx.EXPAND)
        parent.AddSizer(self.sizerCmd, 0, border=4, flag=wx.EXPAND | wx.ALL)

    def _init_coll_lcProps_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=_(u'Property'), width=200)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=_(u'Value'), width=200)

    def _init_sizers(self):
        # generated method, don't edit
        self.sizerMain = wx.BoxSizer(orient=wx.VERTICAL)

        self.sizerCmd = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.szHdr = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_sizerMain_Items(self.sizerMain)
        self._init_coll_sizerCmd_Items(self.sizerCmd)
        self._init_coll_szHdr_Items(self.szHdr)

        self.SetSizer(self.sizerMain)
        self.pnlHdr.SetSizer(self.szHdr)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGRENDERERPROPS,
              name=u'DlgRendererProps', parent=prnt, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1),
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
              title=_(u'Output properties'))

        self.pnlHdr = wx.Panel(id=wxID_DLGRENDERERPROPSPNLHDR, name=u'pnlHdr',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.TAB_TRAVERSAL)
        self.pnlHdr.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.bmpHdr = wx.StaticBitmap(bitmap=wx.ArtProvider.GetBitmap('wxART_EXECUTABLE_FILE',
              wx.ART_TOOLBAR, (32, 32)), id=wxID_DLGRENDERERPROPSBMPHDR,
              name=u'bmpHdr', parent=self.pnlHdr, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self.stHdr = wx.StaticText(id=wxID_DLGRENDERERPROPSSTHDR,
              label=_(u'Edit extended output properties'), name=u'stHdr',
              parent=self.pnlHdr, pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=0)

        self.slHdr = wx.StaticLine(id=wxID_DLGRENDERERPROPSSLHDR, name=u'slHdr',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.lcProps = wx.ListCtrl(id=wxID_DLGRENDERERPROPSLCPROPS,
              name=u'lcProps', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.lcProps.SetMinSize(wx.Size(500, 120))
        self._init_coll_lcProps_Columns(self.lcProps)
        self.lcProps.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivateProperty,
              id=wxID_DLGRENDERERPROPSLCPROPS)

        self.cmdHelp = wx.Button(id=wx.ID_HELP, label=_(u'&Help'),
              name=u'cmdHelp', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)
        self.cmdHelp.Bind(wx.EVT_BUTTON, self.OnCmdHelpButton, id=wx.ID_HELP)

        self.cmdCancel = wx.Button(id=wxID_DLGRENDERERPROPSCMDCANCEL,
              label=_(u'&Cancel'), name=u'cmdCancel', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.cmdCancel.Bind(wx.EVT_BUTTON, self.OnCmdCancelButton,
              id=wxID_DLGRENDERERPROPSCMDCANCEL)

        self.cmdOk = wx.Button(id=wxID_DLGRENDERERPROPSCMDOK, label=_(u'&Ok'),
              name=u'cmdOk', parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1,
              -1), style=0)
        self.cmdOk.Bind(wx.EVT_BUTTON, self.OnCmdOkButton,
              id=wxID_DLGRENDERERPROPSCMDOK)

        self.staticLine = wx.StaticLine(id=wxID_DLGRENDERERPROPSSTATICLINE,
              name=u'staticLine', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self._init_sizers()

    def __init__(self, parent, rendererClass):
        self._init_ctrls(parent)
        self.Bind(wx.EVT_CLOSE, self.OnCmdCancelButton)
        
        font = self.stHdr.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.stHdr.SetFont(font)
        
        self.rendererClass = rendererClass

        self.lcProps.DeleteAllItems()
        savedProps = Settings().GetRenderProperties(rendererClass.__name__)
        for prop in rendererClass.GetProperties():
            value = savedProps.get(prop.lower(), rendererClass.GetProperty(prop))
            self.lcProps.Append([prop, value])
            
            rendererClass.SetProperty(prop, value)
            
        self.SetInitialSize(self.GetEffectiveMinSize())
        self.CentreOnParent()
        
    def OnCmdCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    def OnCmdOkButton(self, event):
        propDict = {}
        for prop in self.rendererClass.GetProperties():
            if self.rendererClass.GetProperty(prop) != self.rendererClass.GetDefaultProperty(prop):
                propDict[prop] = self.rendererClass.GetProperty(prop)

        Settings().SetRenderProperties(self.rendererClass.__name__, propDict)
        self.EndModal(wx.ID_OK)

    def OnActivateProperty(self, event):
        idx = event.GetIndex()
        prop = self.lcProps.GetItemText(idx)
        dlg = wx.TextEntryDialog(self, 
                                 _(u"Edit property"), 
                                 prop, 
                                 unicode(self.rendererClass.GetProperty(prop)))
        if dlg.ShowModal() == wx.ID_OK:
            try:
                value = eval(dlg.GetValue())
            except NameError:
                value = dlg.GetValue()
            except:
                value = self.rendererClass.GetDefaultProperty(prop)
            self.rendererClass.SetProperty(prop, value)
            self.lcProps.SetStringItem(idx, 1, unicode(value))
        dlg.Destroy()
        
    def OnCmdHelpButton(self, event):
        HelpViewer().DisplayID(HelpViewer.ID_RENDER)
        event.Skip()
