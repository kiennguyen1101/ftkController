#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import wx
import ftk_controller_gui

app = wx.App()
title_u = u'FTK Controller'
FTKController = ftk_controller_gui.FTKControllerGUI(None, title=title_u, size=(850, 475))
FTKController.Centre()
FTKController.Show()
FTKController.SetFocus()
app.MainLoop()