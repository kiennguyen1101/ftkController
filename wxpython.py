#! /usr/local/bin/python  -*- coding: UTF-8 -*-
import wx
import pywinauto
import string
import time
from os import path, system
from collections import OrderedDict

APP_EXIT = 1
APP_EXTENSION = 2
config = wx.Config('wxpythonconfig')
config.SetPath('C:/')
print config.GetPath()
if config.Exists('ftk_imager_path'):
    FTK_IMAGER_PATH = config.Read('ftk_imager_path')
else:
    FTK_IMAGER_PATH = "../FTK Imager/FTK Imager.exe"
    config.Write('ftk_imager_path', FTK_IMAGER_PATH)
    
    
class FTKController(wx.Frame):

    doc_extensions = OrderedDict([
       ('.doc', 1), ('.docx', 1), ('.pdf', 1), ('.ppt', 1),
       ('.pptx', 1), ('.xls', 1), ('.xlsx', 1)])
    image_extensions = OrderedDict([
        ('.jpg', 0), ('.jpeg', 0), ('.png', 0),
        ('.bmp', 0), ('.gif', 0)])
    compressed_extensions = OrderedDict([
        ('.rar', 0), ('.zip', 0),
        ('.7z', 0), ('.gz', 0)])
    video_extensions = OrderedDict([
        ('.mpg', 0), ('.mpeg', 0), ('.mp4', 0), ('.avi', 0),
        ('.mov', 0), ('.m4v', 0), ('.mkv', 0), ('.ogv', 0)])
    audio_extensions = OrderedDict([
        ('.mp3', 0), ('.wav', 0), ('.wma', 0), ('.ogg', 0),
        ('.oga', 0), ('.flac', 0), ('.ac3', 0), ('.aac', 0)])
    other_extensions = OrderedDict([('.rtf', 0)])
    all_extensions = OrderedDict([
        ('Document Extensions', doc_extensions),
        ('Image Extensions', image_extensions),
        ('Compressed Extensions', compressed_extensions),
        ('Video Extensions', video_extensions),
        ('Audio Extensions', audio_extensions),
        ('Other Extensions', other_extensions)])

    def __init__(self, *args, **kwargs):
        super(FTKController, self).__init__(*args, **kwargs)

        self.InitMenu()
        self.InitUI()
        self.InitFTKImager()
        self.Centre()
        self.Show()

    def InitMenu(self):
        #First we create a menubar object.
        menubar = wx.MenuBar()
        #Next we create a menu object.
        fileMenu = wx.Menu()
        #Create a menu item. First parameter is parent. Second parameter
        #is the id of the item. Last parameter is help string that is
        #displayed on the statusbar, when the menu item is selected.
        #The & character specifies an accelerator key.
        #The character following the ampersand is underlined.
        #The actual shortcut is defined by the combination of characters.
        #We have specified Ctrl + Q characters. So if we press Ctrl + Q,
        #we close the application. We put a tab character between the &
        #character and the shortcut.
        #This way, we manage to put some space between them.
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+q')

        #Here we set custom icon for the menu item. First, we register an image
        #Afterwards we rescale it using Image.
        #Rescale and convert it to bitmap for use.
        icon = wx.Image('exit.png', wx.BITMAP_TYPE_PNG)
        icon = icon.Rescale(25, 25, wx.IMAGE_QUALITY_HIGH)
        icon = icon.ConvertToBitmap()
        qmi.SetBitmap(icon)

        #We append a menu item into the menu object.
        fileMenu.AppendItem(qmi)
        #We bind the wx.EVT_MENU of the menu item to the custom OnQuit() method.
        #This method will close the application.
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        #After that, we append a menu into the menubar.
        #In the end, we call the SetMenuBar() method. This method
        #belongs to the wx.Frame widget. It sets up the menubar.
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    def InitUI(self):

        panel = wx.Panel(self)

        #This sizer enables explicit positioning of items.
        #Items can also optionally span more than one row and/or column.
        #Constructor: wx.GridBagSizer(integer vgap, integer hgap)
        #The vertical and the horizontal gap defines the space in pixels
        #used among all children.
        sizer = wx.GridBagSizer(5, 5)

        #We add items to the grid with the Add() method.
        #Add(self, item, tuple pos, tuple span=wx.DefaultSpan,
        #integer flag=0, integer border=0, userData=None)
        #Item is a widget that you insert into the grid.
        #The pos specifies the position in the virtual grid.
        #The topleft cell has pos of (0, 0).
        #The span is an optional spanning of the widget.
        #e.g. span of (3, 2) spans a widget across 3 rows and 2 columns.
        #The items in the grid can change their size or keep the default size,
        #when the window is resized. If you want your items to grow and shrink,
        #you can use the following two methods:
        #AddGrowableRow(integer row)
        #AddGrowableCol(integer col)

        bigVBox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        position = [0, 0]
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

        self.ParentCheckBoxes = OrderedDict()
        self.CheckBoxes = OrderedDict()
        setID = 5
        for group, item in self.all_extensions.iteritems():
            self.ParentCheckBoxes[group] = wx.CheckBox(panel, label=group)
            if group == 'Document Extensions':
                self.ParentCheckBoxes[group].SetValue(1)
            sizer.Add(self.ParentCheckBoxes[group], pos=position,
                    flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=10)
            MovePosition(position, 1, 0)
            for extension, value in item.iteritems():
                self.CheckBoxes[extension] = wx.CheckBox(panel, label=extension,
                                                        id=setID)
                setID += 1
                sizer.Add(self.CheckBoxes[extension], pos=AddColumn(position),
                        flag=wx.LEFT | wx.BOTTOM, border=3)
                self.CheckBoxes[extension].SetValue(value)
            MovePosition(position, 0, -len(item))

        bigVBox.Add(sizer)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        buttonOK = wx.Button(panel, label="Ok")
        hbox2.Add(buttonOK)

        buttonRemoveAll = wx.Button(panel, label='Remove All')
        hbox2.Add(buttonRemoveAll, flag=wx.LEFT, border=10)

        bigVBox.Add(hbox2, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)
        self.Bind(wx.EVT_BUTTON, self.OnGetPath, id=buttonGetPath.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=buttonOK.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRemoveAll, id=buttonRemoveAll.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

        panel.SetSizerAndFit(bigVBox)

    def InitFTKImager(self):
        self.pwa_app = pywinauto.application.Application()
        try:
            w_handle = pywinauto.findwindows.find_window(
                class_name='Afx:00400000:0')
        except Exception:
            self.pwa_app.Start(FTK_IMAGER_PATH)
            time.sleep(1)
            w_handle = pywinauto.findwindows.find_window(
                class_name='Afx:00400000:0')
        self.imager = self.pwa_app.window_(handle=w_handle)

    def OnQuit(self, e):
        #Show a dialog that ask user to confirm exit action, default to YES
        dial = wx.MessageDialog(None, 'Do you want to close FTK Imager?', 'Question',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.ExitFTK()
        self.Close()
            
    def OnClose(self, e):
        self.ExitFTK()
        
    def ExitFTK(self):
        self.imager.TypeKeys("%f x", 0.05)

    def OnGetPath(self, e):
        self.GetCustomContentSource()
        if self.custom_content.ItemCount():
            path = self.custom_content.GetItem(0)['text']
            self.textPath.SetValue(path)

    def OnCheck(self, e):
        #Get checkbox checked using GetEventObject()
        ctrl = e.GetEventObject()
        #Check for correct ID.
        #If true: also set all other child checkboxes to corresponding value
        for group, item in self.all_extensions.iteritems():
            if ctrl.GetLabel() == group:
                for k in item.iterkeys():
                    self.CheckBoxes[k].SetValue(ctrl.GetValue())

    def GetCustomContentSource(self):
        if not hasattr(self, 'custom_content'):
            for item in self.imager['ProfUIS-ControlBar5'].Children():
                if type(item) is \
                pywinauto.controls.common_controls.ListViewWrapper:
                    self.custom_content = item
                    break
            if not self.custom_content:
                controlbar = self.imager['ProfUIS-ControlBar4']
                self.custom_content = controlbar.Children()[4]

    def OnOK(self, e):
        path = self.textPath.GetValue()

        if not path:
            dial = wx.MessageDialog(None, 'No path entered', 'Error',
                        wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            return

        amd = string.rsplit(path, '|', 1)

        if len(amd) < 2:
            dial = wx.MessageDialog(None, 'Incorrect path format', 'Error',
                                    wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            return

        if '*' in amd[1]:
            path = amd[0] + '|'

        extensions = []
        for item in self.CheckBoxes.itervalues():
            if item.GetValue():
                extensions.append(item.GetLabel())

        self.imager.SetFocus()
        #for x in range (0, 9):
            #if hasattr(self.imager[x], "Select"):
                #self.custom_content = self.imager[x]
                #break
        self.GetCustomContentSource()
        self.AddExtension(path, extensions)
        w_handle = pywinauto.findwindows.find_windows(
            title=u'FTK Controller')[0]
        window = self.pwa_app.window_(handle=w_handle)
        window.SetFocus()
        dial = wx.MessageDialog(None, 'Completed', 'Info',
                        wx.OK | wx.ICON_INFORMATION)
        dial.ShowModal()

    def OnRemoveAll(self, e):
        if self.imager['&Remove All'].IsEnabled():
            self.imager['&Remove All'].Click()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'FTK Imager')[0]
            window = self.pwa_app.window_(handle=w_handle)
            window['&Yes'].Click()
            
    def OnCreateImage(self, e):
        if not self.imager['&Create Image'].IsEnabled():
            return
        w_handle = pywinauto.findwindows.find_windows(
            title=u'Create Image', class_name='#32770')[0]
        window = self.pwa_app.window_(handle=w_handle)
        window['Checkbox1'].UnCheck()
        window['Checkbox2'].UnCheck()
        window['Checkbox3'].Check()

    def AddExtension(self, path, extensions):
        pos = self.custom_content.ItemCount()
        for item in extensions:
            ctrl = self.imager['&New']
            ctrl.Click()
            self.custom_content.Select(pos)
            ctrl = self.imager['&Edit']
            ctrl.Click()
            w_handle = pywinauto.findwindows.find_window(
                title=u'Wild Card Options')
            editor = self.pwa_app.window_(handle=w_handle)
            editor.Edit.Select()
            source = '%s*%s' % (path, item)
            editor.Edit.SetEditText(source)
            editor['&OK'].Click()
            self.custom_content.Deselect(pos)
            pos += 1


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


if __name__ == '__main__':
    app = wx.App()
    title_u = u'FTK Controller'
    FTKController(None, title=title_u, size=(650, 420))
    app.MainLoop()
