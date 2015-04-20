import pywinauto

pwa_app = pywinauto.application.Application()
w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
imager = pwa_app.window_(handle=w_handle)
imager.SetFocus()