import wx

class TestFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
       
        gs = wx.FlexGridSizer(3,2,10,10) # rows, cols, hgap, vgap
       
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight']

        rb1 = wx.RadioBox(self, 30, "wxRadioBox", wx.DefaultPosition,
wx.DefaultSize, sampleList, 3, wx.RA_SPECIFY_COLS)
        rb2 = wx.RadioBox(self, 31, "", wx.DefaultPosition, wx.DefaultSize, 
                        sampleList, 3, wx.RA_SPECIFY_COLS | wx.NO_BORDER)

        bt1= wx.Button(self, 32, "Butt1")
        bt2= wx.Button(self, 33, "Butt2")
        bt3= wx.Button(self, 34, "Butt3")
        bt4= wx.Button(self, 35, "Butt4")

        gs.AddMany([(bt1, 0, wx.EXPAND),
                    (bt2, 0, wx.EXPAND),
                    (rb1, 0, wx.EXPAND),
                    (bt3, 0, wx.EXPAND),
                    (bt4, 0, wx.EXPAND),
                    (rb2, 0, wx.EXPAND)])
       
        gs.AddGrowableCol(1)
        gs.AddGrowableRow(0)
       
        self.sizer = gs
        self.sizer.Fit(self)
        self.SetAutoLayout(True)
        self.SetSizer(gs)

class MyTestApp(wx.App):
    def OnInit(self):
        self.Frame = TestFrame(None, -1, "RadioBox text")
        self.Frame.Show(True)
        self.SetTopWindow(self.Frame)
        return True

app = MyTestApp(0)
app.MainLoop()