# used library
# wxPython
# turtle


import wx
import colorsys
import turtle as t


class TabPanel1(wx.Panel):
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

class TabPanel2(wx.Panel):
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
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D, name="wxpython")
        self.splitter.SetMinimumPaneSize(200)

        self.panel1 = wx.Panel(self.splitter, -1)
        self.panel1.SetBackgroundColour(wx.LIGHT_GREY)

        self.panel2 = wx.Panel(self.splitter, -1)
        self.panel2.SetBackgroundColour(wx.LIGHT_GREY)

        self.splitter.SplitVertically(self.panel1, self.panel2, sashPosition=800)

        # create tab on panel2
        notebook = wx.Notebook(self.panel2)
        #tabOne = TabPanel1(notebook)
        tabOne = wx.Panel(notebook)
        notebook.AddPage(tabOne, "Tab 1")

        #tabTwo = TabPanel2(notebook)
        tabTwo = wx.Panel(notebook)
        notebook.AddPage(tabTwo, "Tab 2")

        self.color_panel = wx.Panel(tabOne)
        self.hue_slider = wx.Slider(self.color_panel, value=360, minValue=0, maxValue=360)
        self.hue_slider.Bind(wx.EVT_SCROLL, self.on_color_changed)
        self.saturation_slider = wx.Slider(self.color_panel, value=100, minValue=0, maxValue=100)
        self.saturation_slider.Bind(wx.EVT_SCROLL, self.on_color_changed)
        self.value_slider = wx.Slider(self.color_panel, value=100, minValue=0, maxValue=100)
        self.value_slider.Bind(wx.EVT_SCROLL, self.on_color_changed)
        self.html_notation_box = wx.TextCtrl(self.color_panel)
        self.html_notation_box.Disable()

        self.color_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.color_panel_sizer.Add(wx.StaticText(self.color_panel, label="Hue:"))
        self.color_panel_sizer.Add(self.hue_slider)
        self.color_panel_sizer.Add(wx.StaticText(self.color_panel, label="Saturation:"))
        self.color_panel_sizer.Add(self.saturation_slider)
        self.color_panel_sizer.Add(wx.StaticText(self.color_panel, label="Value:"))
        self.color_panel_sizer.Add(self.value_slider)
        self.color_panel_sizer.Add(wx.StaticText(self.color_panel, label="HTML hex code:"))
        self.color_panel_sizer.Add(self.html_notation_box, 0, wx.EXPAND | wx.ALL, 4)
        self.color_panel.SetSizerAndFit(self.color_panel_sizer)

        # tab panel sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, flag=wx.EXPAND)
        self.panel2.SetSizer(sizer)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        #self.Centre()


    def update_scene(self):
        self.Refresh()

    def on_color_changed(self, event):
        hue = self.hue_slider.GetValue()
        saturation = self.saturation_slider.GetValue()
        value = self.value_slider.GetValue()
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(hue/360.0,saturation/100.0, value/100.0)
        html_notation = '#' + hex(256+int(255*self.red))[3:] + hex(256+int(255*self.green))[3:] + hex(256+int(255*self.blue))[3:]
        self.html_notation_box.SetValue(html_notation)
        self.update_scene()

#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.SplitterWindow')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#---------------------------------------------------------------------------

app = MyApp()
app.MainLoop()