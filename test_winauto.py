import pywinauto
import time

start_time = time.time()
path = '\\.\PHYSICALDRIVE0:Basic data partition (5) [190000MB]:NONAME [NTFS]|*'
doc_extensions = ('doc', 'docx', 'pdf', 'xls', 'xlsx')

pwa_app = pywinauto.application.Application()

w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
if (w_handle):
    imager = pwa_app.window_(handle=w_handle)
imager = pwa_app.window_(handle=w_handle)
imager.SetFocus()
# for x in range (0, 9):
#     if hasattr(imager[x], "Select"):
#         custom_content = imager[x]
#         break
#
# for (pos,item) in enumerate(doc_extensions):
#     ctrl = imager['&New']
#     ctrl.Click()
#     custom_content.Select(pos)
#     ctrl = imager['&Edit']
#     ctrl.Click()
#     w_handle = pywinauto.findwindows.find_window(title=u'Wild Card Options')
#     editor = pwa_app.window_(handle=w_handle)
#     editor.Edit.Select
#     source = '%s*.%s' % (path,item)
#     editor.Edit.SetEditText(source)
#     editor['&OK'].Click()
#     custom_content.Deselect(pos)

# failed!
def ftkMainBar():
    for item in imager.Children():
        # if 'ProfUIS-DockBar' in item.FriendlyClassName() and any('Tool' in s for s in item.Texts()):
        #     print item.GetProperties()
        #     print item
        if 'ProfUIS-ControlBar' in item.FriendlyClassName() and not item.Texts()[0]:
            print item
            print item.GetProperties()
            for child in item.Children():
                print child.Texts()


def ftkEvidenceTree():
    for item in imager.Children():
        if 'ControlBar' in item.FriendlyClassName() and any('Evidence' in s for s in item.Texts()):
            print(item.GetProperties())
            treeview = item.Children()[0]
            print treeview.GetProperties()
            print treeview.Roots()

def addAllEvidences():
    imager.TypeKeys("%f l", 0.05)

def removeAllEvidences():
    imager.TypeKeys("%f m", 0.08)

ftkEvidenceTree()
# addAllEvidences()
# removeAllEvidences()
# ftkMainBar()
print time.time() - start_time, "seconds"
