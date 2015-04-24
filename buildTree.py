#!/usr/bin/env python

# This sample classifies the Python keywords alphabetically, using the
# first letter of the keyword (i.e., ``and`` goes into ``a``, ``for``
# goes into ``f`` and so on):
#
# * For each letter, adds a child to the treectrl root
#      * In each child of the root item, adds its corresponding keyword(s)
#

import wx
import keyword
import string
import pywinauto


class TreeFrame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, None, title='FTK Imager Evidence Tree')

        self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                                wx.TR_FULL_ROW_HIGHLIGHT | \
                                                wx.TR_EDIT_LABELS| wx.TR_HIDE_ROOT )

        pwa_app = pywinauto.application.Application()

        w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
        if (w_handle):
            imager = pwa_app.window_(handle=w_handle)
        imager.SetFocus()

        for item in imager.Children():
            if 'ControlBar' in item.FriendlyClassName() and any('Evidence' in s for s in item.Texts()):
                # print(item.GetProperties())
                evidenceTree = item.Children()[0]

        # Add the tree root
        self.root = self.tree_ctrl.AddRoot('Evidences')

        for child in evidenceTree.Roots():
            # self.tree_ctrl.AppendItem(self.root, child.Text())
            self.recursiveTree(root=child, parent=self.root)

        # for kwd in keyword.kwlist:
        #     first = kwd[0]
        #     if first not in letters:
        #         letters.append(first)
        #
        # for letter in letters:
        #     item = tree_ctrl.AppendItem(root, letter)
        #     for kwd in keyword.kwlist:
        #         first = kwd[0]
        #         if first == letter:
        #             sub_item = tree_ctrl.AppendItem(item, kwd)

        self.tree_ctrl.ExpandAll()
        # self.tree_ctrl.Expand(self.root)
        self.Centre()

    def recursiveTree(self, root, parent, _output=None):
        if _output is None:
            _output = []

        children = root.Children()
        # has children
        if len(children) > 0:
            if root.Text() != 'internal_temp':
                node = self.tree_ctrl.AppendItem(parent, root.Text())
            for child in children:
                self.recursiveTree(root=child, parent=node)
        else:
            if root.Text() != 'internal_temp':
                node = self.tree_ctrl.AppendItem(parent, root.Text())
            return


if __name__ == '__main__':
    app = wx.App(0)
    frame = TreeFrame()
    frame.Show()
    app.MainLoop()
