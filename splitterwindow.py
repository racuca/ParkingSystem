import wx
import wx.glcanvas
from OpenGL.GL import glGetString, GL_VERSION


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
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D, name="splitterWindow")
        self.splitter.SetMinimumPaneSize(200)

        self.panel1 = wx.Panel(self.splitter, -1)
        self.panel1.SetBackgroundColour(wx.LIGHT_GREY)

        self.panel2 = wx.Panel(self.splitter, -1)
        self.panel2.SetBackgroundColour(wx.LIGHT_GREY)

        self.splitter.SplitVertically(self.panel1, self.panel2, sashPosition=800)

        # create tab on panel2
        notebook = wx.Notebook(self.panel2)
        tabOne = TabPanel1(notebook)
        notebook.AddPage(tabOne, "Tab 1")

        tabTwo = TabPanel2(notebook)
        notebook.AddPage(tabTwo, "Tab 2")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, flag=wx.EXPAND)
        self.panel2.SetSizer(sizer)


        # create GR Framework OpenGL
        gl_canvas_attribs = [wx.glcanvas.WX_GL_RGBA,
                             wx.glcanvas.WX_GL_DOUBLEBUFFER,
                             wx.glcanvas.WX_GL_DEPTH_SIZE, 16]
        self.gl_canvas = wx.glcanvas.GLCanvas(self.panel1, attribList=gl_canvas_attribs)
        self.gl_context = wx.glcanvas.GLContext(self.gl_canvas)
        self.gl_canvas.SetMinSize((800,600))
        self.gl_canvas.Bind(wx.EVT_PAINT, self.on_paint_gl_canvas)

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_sizer.Add(self.gl_canvas, 1, wx.EXPAND)
        self.panel1.SetSizerAndFit(self.panel_sizer)


        self.Centre()


    def on_paint_gl_canvas(self, evt):
        self.gl_canvas.SetCurrent(self.gl_context)
        print(glGetString(GL_VERSION))

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