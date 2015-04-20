import pywinauto
import time
start_time = time.time()
path = '\\.\PHYSICALDRIVE0:Partition 2 [79894MB]:NONAME [NTFS]|[root]|'
doc_extensions = ('doc', 'docx', 'pdf', 'xls', 'xlsx')

pwa_app = pywinauto.application.Application()
try:
    pwa_app.Connect_(title_re="FTK Imager")
except Exception:
    pwa_app.Start_("C:\Program Files\AccessData\FTK Imager\FTK Imager.exe")
time.sleep(1)
w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
imager = pwa_app.window_(handle=w_handle)
imager.SetFocus()
for x in range (0, 9):
    if hasattr(imager[x], "Select"):    
        custom_content = imager[x]
        break
    
for (pos,item) in enumerate(doc_extensions):
    ctrl = imager['&New']
    ctrl.Click()
    
     
    custom_content.Select(pos)
    ctrl = imager['&Edit']
    ctrl.Click()
    w_handle = pywinauto.findwindows.find_window(title=u'Wild Card Options')
    editor = pwa_app.window_(handle=w_handle)
    editor.Edit.Select
    source = '%s*.%s' % (path,item)
    editor.Edit.SetEditText(source)
    editor['&OK'].Click()
    custom_content.Deselect(pos)

print time.time() - start_time, "seconds"
