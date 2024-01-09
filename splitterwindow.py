import wx


class TabPanel(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))

        btn = wx.Button(self, label="Press Me")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, -1, title, size=(1024, 768))

        #wx.SystemOptions.SetOption("msw.notebook.themed-background", 0)
        #self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        # splitter and two main panel
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D, name="splitterWindow")
        self.splitter.SetMinimumPaneSize(200)

        panel1 = wx.Panel(self.splitter, -1)
        panel1.SetBackgroundColour(wx.LIGHT_GREY)

        panel2 = wx.Panel(self.splitter, -1)
        panel2.SetBackgroundColour(wx.LIGHT_GREY)

        self.splitter.SplitVertically(panel1, panel2, sashPosition=800)

        # create tab on panel2
        notebook = wx.Notebook(panel2)
        tabOne = TabPanel(notebook)
        notebook.AddPage(tabOne, "Tab 1")

        tabTwo = TabPanel(notebook)
        notebook.AddPage(tabTwo, "Tab 2")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)


        self.Centre()

#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.SplitterWindow')
        frame.Show(True)
        self.SetTopWindow(frame)

        return True

#---------------------------------------------------------------------------

app = MyApp(0)
app.MainLoop()