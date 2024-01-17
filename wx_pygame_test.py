# used library
# wxPython
# pygame
import os
import random
import threading
import time

import pygame
import wx
import colorsys

SELF_TEST = 1

class SDLThread:
    def __init__(self, screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.color = (255,0,0)
        self.rect = (10,10,100,100)

    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread1 = threading.Thread(target=self.Run)
        thread1.start()

    def Stop(self):
        self.m_bKeepGoing = False

    def IsRunning(self):
        return self.m_bRunning

    def Run(self):
        while self.m_bKeepGoing:
            if self.screen is None:
                continue
            #if SELF_TEST:
            #    time.sleep(1)
            #    size = self.screen.get_size()
            #    self.rect = (random.randint(0, size[0]),
            #                 random.randint(0, size[1]), 100, 100)
            #e = pygame.event.poll()
            #if e.type == pygame.MOUSEBUTTONDOWN:
            #    self.color = (255, 0, 128)
            #    self.rect = (e.pos[0], e.pos[1], 100, 100)
            #self.screen.fill(self.color, self.rect)
            #pygame.display.flip()
        self.m_bRunning = False

    def setScreen(self, screen):
        self.screen = screen
        self.screen.fill((0,0,0))


class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = parent.GetSize()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.parent.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 1.0
        self.timespacing = int(1000 / self.fps)
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5
        #window = pygame.display.set_mode(self.size)
        self.thread = SDLThread(None)
        self.thread.Start()

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        print("PyGame Redraw", self.size_dirty, self.size)
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False
            self.thread.setScreen(self.screen)

        self.screen.fill((240,240,240))

        cur = 0

        w, h = self.screen.get_size()
        #while cur <= h:
        #    pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))
        #    cur += self.linespacing
        rect = pygame.Rect(random.randint(0, self.size[0]),
                           random.randint(0, self.size[1]), 100, 100)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.Image(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.Bitmap(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self.parent)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.parent.GetSize()
        print("PyGame panel", self.size)
        self.size_dirty = True
        self.Redraw()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        #self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source=self.timer)
        self.thread.Stop()

class TabPanel1(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))
        self.SetBackgroundColour("white")

        btn = wx.Button(self, label="Press Me Tab 1")

        self.Bind(wx.EVT_BUTTON, self.onClick, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    def onClick(self, event):
        pass

class TabPanel2(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))
        self.SetBackgroundColour("white")

        btn = wx.Button(self, label="Press Me Tab 2")
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
        self.panel2 = wx.Panel(self.splitter, -1)
        self.splitter.SplitVertically(self.panel1, self.panel2, sashPosition=800)

        # create tab on panel2
        notebook = wx.Notebook(self.panel2)
        tabOne = TabPanel1(notebook)
        notebook.AddPage(tabOne, "Tab 1")
        tabTwo = TabPanel2(notebook)
        notebook.AddPage(tabTwo, "Tab 2")

        self.display = PygameDisplay(self.panel1, -1)

        # tab panel sizer
        tabsizer = wx.BoxSizer(wx.VERTICAL)
        tabsizer.Add(notebook, 1, flag=wx.EXPAND)
        self.panel2.SetSizer(tabsizer)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

    def Kill(self, event):
        self.display.Kill(event)
        self.Destroy()

    def OnSize(self, event):
        self.Layout()
        #self.display = PygameDisplay(self.panel1, -1)

    def Update(self, event):
        self.curframe += 1
        self.statusbar.SetStatusText("Frame %i" % self.curframe, 2)

    def OnScroll(self, event):
        self.display.linespacing = self.slider.GetValue()


#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, id=-1, title='wx.SplitterWindow')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#---------------------------------------------------------------------------
pygame.init()
app = MyApp()
app.MainLoop()