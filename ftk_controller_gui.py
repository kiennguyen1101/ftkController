#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import string
import os
import ConfigParser
import time
from collections import OrderedDict
import csv
import traceback
import wx
from ftk_controller import FTKController
from libs import admin

class FTKControllerGUI(wx.Frame):
    APP_EXTENSION = 12
    APP_FTK_PATH = 13

    def __init__(self, *args, **kwargs):
        super(FTKControllerGUI, self).__init__(*args, **kwargs)
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create pages and append to notebook
        mainPage = PageMain(nb)
        usbPage = PageUSB(nb)
        nb.AddPage(mainPage, "Main")
        nb.AddPage(usbPage, "USB")

        # sizer
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.InitMenu()
        self.Centre()
        self.Show()

    def InitMenu(self):
        # Ccreate a menubar object.
        menubar = wx.MenuBar()
        # Create a menu object.
        fileMenu = wx.Menu()
        optionMenu = wx.Menu()
        # Create a menu item with shortkey ctrl+Q
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+q')

        # Set custom icon for the menu item
        try:
            icon = wx.Image('exit.png', wx.BITMAP_TYPE_PNG)
            icon = icon.Rescale(25, 25, wx.IMAGE_QUALITY_HIGH)
            icon = icon.ConvertToBitmap()
            qmi.SetBitmap(icon)
        except Exception:
            self.ShowError('Cannot find "exit.png"')
            pass

        #Append a menu item into the menu object.
        fileMenu.AppendItem(qmi)
        #Bind the menu item to the custom OnQuit() method.
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)

        menu = wx.MenuItem(optionMenu, self.APP_EXTENSION, 'Extensions')
        optionMenu.AppendItem(menu)
        self.Bind(wx.EVT_MENU, self.OnOptionExtension, id=self.APP_EXTENSION)

        menu = wx.MenuItem(optionMenu, self.APP_FTK_PATH, 'FTK Imager Path')
        optionMenu.AppendItem(menu)
        self.Bind(wx.EVT_MENU, self.OnOptionPath, id=self.APP_FTK_PATH)

        #Append a menu into the menubar and finalize settings
        menubar.Append(fileMenu, '&File')
        menubar.Append(optionMenu, '&Options')
        self.SetMenuBar(menubar)


    def OnQuit(self, e):
        # Show a dialog that ask user to confirm exit action, default to YES
        dial = wx.MessageDialog(None, 'Do you want to close FTK Imager?', 'Question',
                                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            FTKController.ExitFTK()
        self.Close()
        exit()


    # ----------------------------------------------------------------------
    def OnOptionExtension(self, e):
        """"""


    # ----------------------------------------------------------------------
    def OnOptionPath(self, e):
        """"""


class GaugeDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(GaugeDialog, self).__init__(*args, **kwargs)

        self.initUI()
        self.SetSize((250, 200))

    def initUI(self):
        self.Centre()
        self.Show(True)

        pnl = wx.Panel(self)
        bigVBox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(pnl, 100, size=(225, 25))
        self.btnOk = wx.Button(pnl, wx.ID_OK)
        self.text = wx.StaticText(pnl, label="Standby")
        hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
        hbox3.Add(self.btnOk, proportion=1, flag=wx.RIGHT, border=10)
        hbox2.Add(self.text, proportion=1)
        bigVBox.Add((0, 30))
        bigVBox.Add(hbox1, flag=wx.ALIGN_CENTRE, border=10)
        bigVBox.Add((0, 20))
        bigVBox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
        bigVBox.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTRE)

        pnl.SetSizer(bigVBox)


def AddRow(pos, rownum=1):
    if not pos:
        return False
    if len(pos) != 2:
        return False
    pos[0] = pos[0] + rownum
    return pos


def AddColumn(pos, colnum=1):
    if not pos:
        return False
    if len(pos) != 2:
        return False
    pos[1] = pos[1] + colnum
    return pos


def MovePosition(pos, row=1, col=1):
    if not pos:
        return False
    if len(pos) != 2:
        return False
    pos[0] = pos[0] + row
    pos[1] = pos[1] + col
    return pos


########################################################################
class PageMain(wx.Panel):
    FTKImager = None
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.InitFTKImager()
        self.GetExtensions()
        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        # Set up a big vertical box that will cover up the whole panel.
        # Each row will be a horizontal subset of this box
        bigVBox = wx.BoxSizer(wx.VERTICAL)

        # H box containing path
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        text1 = wx.StaticText(panel, label="Path")
        hbox1.Add(text1, flag=wx.LEFT | wx.BOTTOM,
                  border=5)

        #pos: (0, 1)
        self.textPath = wx.TextCtrl(panel)
        hbox1.Add(self.textPath, proportion=3, border=10,
                  flag=wx.EXPAND | wx.LEFT)

        buttonGetPath = wx.Button(panel, label="Get Path")
        hbox1.Add(buttonGetPath, proportion=1, border=5, flag=wx.LEFT)

        #        sizer.Add(hbox1, pos=position, flag=wx.LEFT | wx.TOP, border=10)
        bigVBox.Add(hbox1, flag=wx.LEFT | wx.TOP, border=10)

        #pos: (1, 0)
        line = wx.StaticLine(panel)
        bigVBox.Add(line, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)

        #This sizer enables explicit positioning of items
        sizer = wx.GridBagSizer(5, 5)
        # wrap the bagsizer with a horizontal box
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(sizer)
        bigVBox.Add(hbox2)

        #group checkboxes and put them in attribute so we can access them later.
        self.ParentCheckBoxes = OrderedDict()
        self.CheckBoxes = OrderedDict()
        #ID for checkboxes
        setID = 5
        #original position for bag sizer
        position = [0, 0]

        #loop through all extensions dict
        for group, item in self.all_extensions.iteritems():
            if not len(item):
                pass
            self.ParentCheckBoxes[group] = wx.CheckBox(panel, label=group)
            #add parent checkbox and move position down 1 row
            sizer.Add(self.ParentCheckBoxes[group], pos=position,
                      flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=10)
            MovePosition(position, 1, 0)
            #add child checkboxes for the group each in same row but different column
            for extension, value in item.iteritems():
                self.CheckBoxes[extension] = wx.CheckBox(panel, label=extension,
                                                         id=setID)
                setID += 1
                sizer.Add(self.CheckBoxes[extension], pos=AddColumn(position),
                          flag=wx.LEFT | wx.BOTTOM, border=3)
                self.CheckBoxes[extension].SetValue(int(value))
            #Move position back to first column
            MovePosition(position, 0, -len(item))


        #add 2 buttons. Again, these buttons are wrapped in h box
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        buttonOK = wx.Button(panel, label="Ok")
        buttonRemoveAll = wx.Button(panel, label='Remove All')
        buttonCreateImage = wx.Button(panel, label='Create Image')
        hbox3.Add(buttonOK)
        hbox3.Add(buttonRemoveAll, flag=wx.LEFT, border=10)
        hbox3.Add(buttonCreateImage, flag=wx.LEFT, border=10)
        bigVBox.Add(hbox3, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)

        #bind events to various functions
        self.Bind(wx.EVT_BUTTON, self.OnGetPath, id=buttonGetPath.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=buttonOK.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=buttonRemoveAll.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnCreateImage, id=buttonCreateImage.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

        #set main sizer of the panel
        panel.SetSizerAndFit(bigVBox)


    def GetExtensions(self):
        with open('extensions.csv', 'rb') as extensionFile:
            extensionReader = csv.reader(extensionFile)
            # skip the header
            next(extensionReader, None)

            self.all_extensions = OrderedDict([])

            for row in extensionReader:
                exdict = OrderedDict({row[1]: row[2]})
                temp = {}
                if self.all_extensions.has_key(row[0]):
                    temp = self.all_extensions[row[0]]
                self.all_extensions.update({row[0]: OrderedDict(exdict.items() + temp.items())})

                # exit()

    def InitFTKImager(self):
        filePath = self.ReadConfig()
        self.FTKImager = FTKController()

        if not admin.isUserAdmin():
            self.ShowError("This program needs to be started as administrator")
            # rc = admin.runAsAdmin(cmdLine=("C:\Program Files (x86)\AccessData\FTK Imager\FTK Imager.exe", ""))
            admin.runAsAdmin()
            exit(0)
        else:
            if self.FTKImager.CheckFTKImagerStarted():
                return
            else:
                for i in range(0, 15):
                    if self.FTKImager.StartProgramElavated(filePath):
                        break
                        time.sleep(0.5)

        # is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        # if not is_admin:
        # self.ShowError("Please start FTK Imager first or run this program as administrator")
        # self.Close()


    def ReadConfig(self, configFile='config.ini'):
        FTK_IMAGER_PATH = False
        try:
            # read config.ini for path to FTK Imager
            config = ConfigParser.ConfigParser(dict_type=MultiOrderedDict)
            config.read(configFile)
            path = config.get('DEFAULT', 'path')
            for item in path:
                if os.path.exists(item):
                    FTK_IMAGER_PATH = item
        except BaseException:
            import sys

            print "Unexpected error:", sys.exc_info()[0]
            self.ShowError('Error reading file ' + configFile)
            exit(0)
        finally:
            return FTK_IMAGER_PATH

    def OnQuit(self, e):
        # Show a dialog that ask user to confirm exit action, default to YES
        dial = wx.MessageDialog(None, 'Do you want to close FTK Imager?', 'Question',
                                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.FTKImager.ExitFTK()
        self.Close()
        exit()

    def OnClose(self, e):
        self.Close()
        exit()

    def OnCheck(self, e):
        # Get checkbox checked using GetEventObject()
        ctrl = e.GetEventObject()
        # Check for correct ID.
        # If true: also set all other child checkboxes to corresponding value
        for group, item in self.all_extensions.iteritems():
            if ctrl.GetLabel() == group:
                for k in item.iterkeys():
                    self.CheckBoxes[k].SetValue(ctrl.GetValue())

    def OnGetPath(self, e):
        try:
            if self.FTKImager.GetCustomContentSource(1):
                itemCount = self.FTKImager.custom_content.ItemCount()

            if not itemCount:
                self.ShowError("Cannot select custom content list")
                return
            # Get path from the custom content first item
            path = self.FTKImager.custom_content.GetItem(0)['text']
            self.textPath.SetValue(path)
            self.FTKImager.custom_content.Select(0)
            if self.FTKImager.imager['&Remove'].IsEnabled():
                self.FTKImager.imager['&Remove'].Click()
                # w_handle = pywinauto.findwindows.find_windows(
                # title=u'FTK Imager')[0]
                #window = self.pwa_app.window_(handle=w_handle)
                #window['&Yes'].Click()
        except Exception:
            self.ShowError("Cannot select custom content list")

    def OnOK(self, e):
        try:
            path = self.textPath.GetValue()

            if not path:
                self.ShowError('No path entered')
                return

            amd = string.rsplit(path, '|', 1)

            if len(amd) < 2:
                self.ShowError('Incorrect path format')
                return

            if '*' in amd[1]:
                path = amd[0] + '|'

            extensions = []
            for item in self.CheckBoxes.itervalues():
                if item.GetValue():
                    extensions.append(item.GetLabel())

            if not len(extensions):
                self.ShowError('No extensions selected')
                return

            if not self.FTKImager.custom_content:
                self.FTKImager.GetCustomContentSource()

            # minimize imager, show a progress dialog and show imager after adding
            self.FTKImager.imager.Minimize()
            self.Gdial = wx.ProgressDialog('Adding extensions', 'Adding extensions',
                                           maximum=100, parent=self, style=wx.PD_APP_MODAL | wx.PD_CAN_ABORT
                                                                           | wx.PD_SMOOTH)
            percentage = 1 / float(len(extensions)) * 100
            count = percentage
            for item in extensions:
                self.FTKImager.AddExtension(path, item)
                # Update() returns a tuple of bool (continue, skip)
                if not self.Gdial.Update(count)[0]:
                    break
                count += percentage
            self.Gdial.Update(100)
            self.Gdial.Destroy()
            self.FTKImager.ExtensionAddFinish()
        except Exception, err:
            print traceback.format_exc()
            #or
    def OnRemoveAll(self, e):
        self.FTKImager.RemoveAll()

    def OnCreateImage(self, e):
        self.FTKImager.CreateImage()

    def ShowNotification(self, message):
        Xmessage = wx.MessageDialog(None, message, 'Event', wx.OK | wx.ICON_INFORMATION)
        Xmessage.ShowModal()
        pass

    def ShowError(self, message):
        error_message = wx.MessageDialog(None, message, 'Error',
                                         wx.OK | wx.ICON_ERROR)
        error_message.ShowModal()


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)


########################################################################
class PageUSB(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)