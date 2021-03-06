#! /usr/local/bin/python  -*- coding: UTF-8 -*-
from collections import OrderedDict
import csv
import os.path
import string

import wx


class GUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        self.GetExtensions()
        self.InitMenu()
        self.InitUI()
        self.Centre()
        self.Show()

    # Get all the pre-defined extensions for UI
    def GetExtensions(self):
        with open('extensions.csv', 'rb') as extensionFile:
            extensionReader = csv.reader(extensionFile)
            # skip the header
            next(extensionReader, None)

            self.all_extensions = OrderedDict([])

            # audio_extensions = OrderedDict([
            # ('.mp3', 0), ('.wav', 0), ('.wma', 0), ('.ogg', 0),
            #     ('.oga', 0), ('.flac', 0), ('.ac3', 0), ('.aac', 0)
            # ])
            # other_extensions = OrderedDict([('.pst', 0)])
            # all_extensions = OrderedDict([
            #     ('MSOffice Extensions', msdoc_extensions),
            #     ('Audio Extensions', audio_extensions),
            #     ('Other Extensions', other_extensions)
            # ])
            for row in extensionReader:
                exdict = OrderedDict({row[1]: row[2]})
                temp = {}
                if self.all_extensions.has_key(row[0]):
                    temp = self.all_extensions[row[0]]
                self.all_extensions.update({row[0]: OrderedDict(exdict.items() + temp.items())})

    def InitMenu(self):
        # First we create a menubar object.
        menubar = wx.MenuBar()
        # Next we create a menu object.
        fileMenu = wx.Menu()
        # Create a menu item
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+q')

        # Set custom icon for the menu item
        try:
            icon = wx.Image('exit.png', wx.BITMAP_TYPE_PNG)
            icon = icon.Rescale(25, 25, wx.IMAGE_QUALITY_HIGH)
            icon = icon.ConvertToBitmap()
            qmi.SetBitmap(icon)
        except Exception:
            # todo: more specific exception handling
            self.ShowError('Cannot find "exit.png"')
            pass

        # We append a menu item into the menu object.
        fileMenu.AppendItem(qmi)
        #We bind the wx.EVT_MENU of the menu item to the custom OnQuit() method.
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        #After that, we append a menu into the menubar
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

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

        #This sizer enables explicit positioning of items.
        sizer = wx.GridBagSizer(5, 5)
        #we'll wrap the bagsizer with a horizontal box
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
            self.MovePosition(position, 1, 0)
            #add child checkboxes for the group each in same row but different column
            for extension, value in item.iteritems():
                self.CheckBoxes[extension] = wx.CheckBox(panel, label=extension,
                                                         id=setID)
                setID += 1
                sizer.Add(self.CheckBoxes[extension], pos=self.AddColumn(position),
                          flag=wx.LEFT | wx.BOTTOM, border=3)
                self.CheckBoxes[extension].SetValue(int(value))
            #Move position back to first column
            self.MovePosition(position, 0, -len(item))


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

    def OnGetPath(self, e):
        # return if self.custom_content is not set
        if not self.GetCustomContentSource():
            self.ShowError('Cannot get path from custom content source')
            return

        # Get path from the custom content first item

        try:
            if self.custom_content.ItemCount():
                path = self.custom_content.GetItem(0)['text']
                self.textPath.SetValue(path)
                self.custom_content.Select(0)
                if self.imager['&Remove'].IsEnabled():
                    self.imager['&Remove'].Click()
                    #w_handle = pywinauto.findwindows.find_windows(
                    #title=u'FTK Imager')[0]
                    #window = self.pwa_app.window_(handle=w_handle)
                    #window['&Yes'].Click()
        except:
            pass

    def OnQuit(self, e):
        # Show a dialog that ask user to confirm exit action, default to YES
        dial = wx.MessageDialog(None, 'Do you want to close FTK Imager?', 'Question',
                                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.ExitFTK()
        self.Close()

    def OnClose(self, e):
        self.ExitFTK()

    def OnCheck(self, e):
        # Get checkbox checked using GetEventObject()
        ctrl = e.GetEventObject()
        # Check for correct ID.
        # If true: also set all other child checkboxes to corresponding value
        for group, item in self.all_extensions.iteritems():
            if ctrl.GetLabel() == group:
                for k in item.iterkeys():
                    self.CheckBoxes[k].SetValue(ctrl.GetValue())

    def OnRemoveAll(self, e):
        try:
            if self.imager['&Remove All'].IsEnabled():
                self.imager['&Remove All'].Click()
                w_handle = pywinauto.findwindows.find_windows(
                    title=u'FTK Imager')[0]
                window = self.pwa_app.window_(handle=w_handle)
                window['&Yes'].Click()
        except Exception:
            pass

    def OnOK(self, e):
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

            # self.imager.SetFocus()
            # for x in range (0, 9):
            # if hasattr(self.imager[x], "Select"):
            #self.custom_content = self.imager[x]
            #break

        if not self.GetCustomContentSource():
            return

        # minimize imager, show a progress dialog and show imager after adding
        self.imager.Minimize()
        self.Gdial = wx.ProgressDialog('Adding extensions', 'Adding extensions',
                                       maximum=100, parent=self, style=wx.PD_APP_MODAL | wx.PD_CAN_ABORT
                                                                       | wx.PD_SMOOTH)
        self.AddExtension(path, extensions)
        self.Gdial.Destroy()
        self.imager.Restore()
        w_handle = pywinauto.findwindows.find_windows(
            title=u'FTK Controller')[0]
        window = self.pwa_app.window_(handle=w_handle)
        window.SetFocus()

    def OnCreateImage(self, e):
        if not self.imager['&Create Image'].IsEnabled():
            return
        try:
            self.imager['&Create Image'].Click()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'Create Image', class_name='#32770')[0]
            createWindow = self.pwa_app.window_(handle=w_handle)
            createWindow['Checkbox1'].UnCheck()
            createWindow['Checkbox2'].UnCheck()
            createWindow['Checkbox3'].Check()
            createWindow['&Add...'].Click()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'Evidence Item Information', class_name='#32770')[0]
            window = self.pwa_app.window_(handle=w_handle)
            window['&Next >'].Click()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'Select Image Destination', class_name='#32770')[0]
            window = self.pwa_app.window_(handle=w_handle)
        except:
            pass
        path = os.path.realpath('../../')
        dataPath = path + '\ImageData'
        try:
            os.stat(dataPath)
        except OSError, e:
            os.mkdir(dataPath)
        window['Edit'].Select()
        window['Edit'].SetEditText(dataPath)
        window['Edit2'].Select()
        fileName = time.strftime('%H%M %d-%m-%Y', time.localtime())
        window['Edit2'].SetEditText(fileName)
        window['Edit4'].Select()
        window['Edit4'].SetEditText('0')
        window['&Finish'].Click()

        createWindow['&Start'].Click()
        self.ShowNotification('Image created: ' + dataPath + '\\' + fileName + '.ad1')

    def ShowError(self, message):
        error_message = wx.MessageDialog(None, message, 'Error',
                                         wx.OK | wx.ICON_ERROR)
        error_message.ShowModal()

    def ShowNotification(self, message):
        Xmessage = wx.MessageDialog(None, message, 'Event', wx.OK | wx.ICON_INFORMATION)
        Xmessage.ShowModal()
        pass

    def AddRow(self, pos, rownum=1):
        if not pos:
            return False
        if len(pos) != 2:
            return False
        pos[0] = pos[0] + rownum
        return pos

    def AddColumn(self, pos, colnum=1):
        if not pos:
            return False
        if len(pos) != 2:
            return False
        pos[1] = pos[1] + colnum
        return pos

    def MovePosition(self, pos, row=1, col=1):
        if not pos:
            return False
        if len(pos) != 2:
            return False
        pos[0] = pos[0] + row
        pos[1] = pos[1] + col
        return pos


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