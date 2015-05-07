#!/usr/bin/env python

# This sample classifies the Python keywords alphabetically, using the
# first letter of the keyword (i.e., ``and`` goes into ``a``, ``for``
# goes into ``f`` and so on):
#
# * For each letter, adds a child to the treectrl root
#      * In each child of the root item, adds its corresponding keyword(s)
#

import wx
import time
import pywinauto

menuItems = ('Add Path')

class TreeFrame(wx.Frame):
    def __init__(self):

        self.Frame = wx.Frame.__init__(self, None, title='FTK Imager Evidence Tree')

        self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS |\
                                                wx.TR_FULL_ROW_HIGHLIGHT | \
                                                wx.TR_EDIT_LABELS| wx.TR_HIDE_ROOT )

        pwa_app = pywinauto.application.Application()

        w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
        if (w_handle):
            imager = pwa_app.window_(handle=w_handle)
            imager.Minimize()
        # imager.SetFocus()


        for item in imager.Children():
            if 'ControlBar' in item.FriendlyClassName() and any('Evidence' in s for s in item.Texts()):
                # print(item.GetProperties())
                evidenceTree = item.Children()[0]

        # Add the tree root
        self.root = self.tree_ctrl.AddRoot('Evidences')
        if len(evidenceTree.Roots()) <= 0:
            imager.TypeKeys("%f l", 0.05)
            busyDlg = wx.BusyInfo("Please wait")
            time.sleep(1)
            busyDlg.Destroy()

        for child in evidenceTree.Roots():
            # self.tree_ctrl.AppendItem(self.root, child.Text())
            self.recursiveAdd(root=child, parent=self.root)

        self.tree_ctrl.ExpandAll()
        # self.tree_ctrl.Expand(self.root)
        self.Centre()
        # register the self.onActivated function to be called on double click
        wx.EVT_TREE_ITEM_ACTIVATED(self.tree_ctrl, self.tree_ctrl.GetId(), self.onActivated)
        wx.EVT_TREE_ITEM_RIGHT_CLICK(self.tree_ctrl, self.tree_ctrl.GetId(), self.onRightClick)
        wx.EVT_TREE_KEY_DOWN(self.tree_ctrl, self.tree_ctrl.GetId(), self.onKeyDown)
        self._menu = None

        # ### 2. Launcher creates wxMenu. ###
        # menu = wx.wxMenu()
        # ### 3. Launcher packs menu with Append. ###
        # menu.Append( id, title )
        # ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
        # wx.EVT_MENU( menu, id, self.MenuSelectionCb )
        # ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        # self.frame.PopupMenu( menu, event.GetPoint() )
        # # destroy to avoid mem leak#
        # menu.Destroy()

    def onKeyDown(self, event):
        print "asdfsadf"
        print event.GetKeyCode()
        print event.GetItem()

    def onRightClick(self, event):
        print self.tree_ctrl.GetItemText(event.GetItem())
        menu = wx.Menu()
        id = wx.NewId()
        menu.Append(id, "Hello")
        wx.EVT_MENU(menu, id , self.MenuSelectionCb)
        self.PopupMenu(menu, event.GetPoint())
        menu.Destroy()

    def onActivated(self, event):
        ### 1. Get what is clicked/selected
        itemID = event.GetItem()
        if not itemID.IsOk():
            itemID = self.tree_ctrl.GetSelection()
        self.tree_ctrl.ToggleItemSelection(itemID)
        title = self.tree_ctrl.GetItemText(itemID)
        print title
        # self.ClientToScreen(event.GetPoint())

    def MenuSelectionCb(self, event):
        # do something
        print "asdflkj"
        print event.GetString()

    def recursiveAdd(self, root, parent, _output=None):
        if _output is None:
            _output = []

        children = root.Children()
        # has children
        if len(children) > 0:
            if root.Text() != 'internal_temp':
                node = self.tree_ctrl.AppendItem(parent, root.Text())
            for child in children:
                self.recursiveAdd(root=child, parent=node)
        else:
            if root.Text() != 'internal_temp':
                node = self.tree_ctrl.AppendItem(parent, root.Text())
            return


if __name__ == '__main__':
    app = wx.App(0)
    frame = TreeFrame()
    frame.Show()
    app.MainLoop()
