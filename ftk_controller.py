import time
import os
import traceback
import pywinauto
import logging
########################################################################
class FTKController(object):
    """"""
    findContentMethods = 2
    imager = None
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.pwa_app = pywinauto.application.Application()

    def HookFTKImager(self):
        """"""
        # bind pywinauto to FTK Imager if it has already been started
        #else try to start FTK Imager.
        w_handle = False
        try:
            w_handle = pywinauto.findwindows.find_window(
                class_name='Afx:00400000:0')
            if (w_handle):
                self.imager = self.pwa_app.window_(handle=w_handle)
                return True
        except Exception, ex:
            return False
      

    def StartProgramElavated(self, path):
        # bind pywinauto to FTK Imager if it has already been started
        # else try to start FTK Imager.
        w_handle = False
        try:
            self.pwa_app.Start(path)
            time.sleep(1)
            w_handle = pywinauto.findwindows.find_window(
                class_name='Afx:00400000:0')
        except Exception:
            logging.exception("Cannot start FTK Imager")
            return False
        finally:
            if not w_handle:
                return False
            self.imager = self.pwa_app.window_(handle=w_handle)
            return True

    def ExitFTK(self):
        self.imager.TypeKeys("%f x", 0.05)

    def GetCustomContentSource(self, itemCount=0):
        #Try to get the custom content source from control bars 
        #if no attributes is stored.
        #TODO: Check custom content source from undock (seperate) windows
        try:
            for item in self.imager.Children():               
                if type(item) is pywinauto.controls.common_controls.ListViewWrapper:
                    # print item.ItemCount()
                    # Check if the item's text list contains this string                   
                    if "Evidence:File System" in item.GetColumn(0)['text']:
                        logging.info("Found custom content")
                        self.custom_content = item                        
                        return True
        except Exception, e:
            logging.exception("Error getting custom content")
            return False

    def AddExtension(self, path, extension):        
        pos = self.custom_content.ItemCount()
        ctrl = self.imager['&New']
        ctrl.Click()
        self.custom_content.Select(pos)
        ctrl = self.imager['&Edit']
        ctrl.Click()
        w_handle = pywinauto.findwindows.find_window(
            title=u'Wild Card Options')
        editor = self.pwa_app.window_(handle=w_handle)
        editor.Edit.Select()
        source = '%s*.%s' % (path, extension)
        editor.Edit.SetEditText(source)
        editor['&OK'].Click()
        self.custom_content.Deselect(pos)

    def ExtensionAddFinish(self):
        self.imager.Restore()
        w_handle = pywinauto.findwindows.find_windows(
            title=u'FTK Controller')[0]
        window = self.pwa_app.window_(handle=w_handle)
        window.SetFocus()

    def CreateImage(self):
        if not self.imager['&Create Image'].IsEnabled():
            return
        
        #TODO: Test creating multiple images simultaneously
        self.imager['&Create Image'].Click()
        w_handle = pywinauto.findwindows.find_windows(
            title=u'Create Image', class_name='#32770')[0]
        createWindow = self.pwa_app.window_(handle=w_handle)
        #TODO: options for these checkboxes
        #Checkbox1 = Verify images after created
        #Checkbox2 = Precalculate Progress Statistics
        #Checkbox3 = Create directory listings of all files in the image after they are created
        createWindow['Checkbox1'].UnCheck()
        createWindow['Checkbox2'].Check()
        createWindow['Checkbox3'].UnCheck()
        createWindow['&Add...'].Click()
        w_handle = pywinauto.findwindows.find_windows(
            title=u'Evidence Item Information', class_name='#32770')[0]
        window = self.pwa_app.window_(handle=w_handle)        
        window['&Next >'].Click() 
        w_handle = pywinauto.findwindows.find_windows(
            title=u'Select Image Destination', class_name='#32770')[0]
        window = self.pwa_app.window_(handle=w_handle)
        
        #TODO: We need options for these as well
        #Edit = Image Destination Folder
        #Edit2 = Image File name (Exclude extension)
        #Edit3 = Image Fragment Size (MB)
        #Edit4 = Compression
        #Checkbox = Use AD Encryption
        #Checkbox2 = Filter by File Owner
        path = os.path.realpath('../../')
        dataPath = path + '\ImageData'
        try:
            os.stat(dataPath)
        except OSError, e:
            logging.exception("Cannot find ImageData directory.")
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

    def RemoveAll(self):        
        if self.imager['&Remove All'].IsEnabled():
            self.imager['&Remove All'].Click()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'FTK Imager')[0]
            window = self.pwa_app.window_(handle=w_handle)
            window['&Yes'].Click()
       
    def AddEvidences(self):
        for item in self.imager.Children():
            if 'ControlBar' in item.FriendlyClassName() and any('Evidence' in s for s in item.Texts()):
                logging.debug("Found evidence tree")                
                evidenceTree = item.Children()[0]        
                
        # Add all evidences in FTK Imager
        if len(evidenceTree.Roots()) <= 0:
            self.imager.TypeKeys("%f l", 0.05)
            
        return evidenceTree