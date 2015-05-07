import pywinauto
import time

start_time = time.time()
path = '\\.\PHYSICALDRIVE0:Basic data partition (5) [190000MB]:NONAME [NTFS]|*'
doc_extensions = ('doc', 'docx', 'pdf', 'xls', 'xlsx')

pwa_app = pywinauto.application.Application()

w_handle = pywinauto.findwindows.find_window(class_name='Afx:00400000:0')
# if (w_handle):
# imager = pwa_app.window_(handle=w_handle)
imager = pwa_app.window_(handle=w_handle)
imager.SetFocus()
# for x in range (0, 9):
# if hasattr(imager[x], "Select"):
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
        if any('Tool' in s for s in item.Texts()):
            print item.GetProperties()
            print item



def ftkEvidenceTree():
    for item in imager.Children():
        if 'ControlBar' in item.FriendlyClassName() and any('Evidence' in s for s in item.Texts()):
            # print(item.GetProperties())
            treeview = item.Children()[0]
            print treeview.GetProperties()
            root = treeview.Roots()[0]

    # print root.Text()
    recursiveTree(root)
    # if len(root.Children()) > 0:
    #     child1 = root.Children()[0]
    #     # for child in root.SubElements():
    #     #     if child.Text() != 'internal_temp':
    #     #         print child.Text()
    #     # print child1.Text()
    #     child = child1
    #     while child.Next() is not None:
    #         print child.Text()
    #         drawOneLevel(child)
    #         child = child.Next()


def drawOneLevel(root, _output=None):
    if _output is None:
        _output = []

    #do some work here, add to your list
    for child in root.Children():
        print "\t" + child.Text()

    max = 0
    if max <= 0:  #Some condition where the recursion stops
        return _output
        # else:        #recurse with new arguments so that we'll stop someday...
        #     return recursiveTree(max-1, _output=_output)


def recursiveTree(root, _output=None, level = 0):
    if _output is None:
        _output = []

    if root.Text() != 'internal_temp':
        print "  "*level + root.Text()
    # sibling = root
    #
    # while sibling.Next() is not None:
    #     print sibling.Text()
    #     sibling = sibling.Next()

    children = root.Children()
    # has children
    if len(children) > 0:
        for child in children:
            recursiveTree(child, level=level+1)
    else:
        return

def addAllEvidences():
    imager.TypeKeys("%f l", 0.05)


def removeAllEvidences():
    imager.TypeKeys("%f m", 0.08)

# ftkEvidenceTree()
# addAllEvidences()
# removeAllEvidences()
# ftkMainBar()
# print imager.TreeView.Texts()
# toolbar = imager.ToolBar.Children()[0]
# rect = toolbar.ClientRect()
# toolbar.ReleaseMouseInput(coords=(rect.left+44, rect.top+9))
# print(toolbar.GetShowState())
# imager.Restore()
# imager.SetFocus()
# imager.Wait('visible')
# toolbar.Click(coords=(rect.left+44, rect.top+9))
# imager.Minimize()
# print time.time() - start_time, "seconds"
