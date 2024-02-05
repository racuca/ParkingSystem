# used library
# wxPython
# pygame

# Traffic Control System  - Parking Manager
# 

import os
import random
import threading
import time
from enum import IntEnum

import pygame
import wx
import colorsys

SELF_TEST = 1

# 도형 Type
class FigureType(IntEnum):
    Rect = 0         # 직사각형
    Square = 1       # 정사각형
    Triangle = 3     # 삼각형
    Eq_Triangle = 2  # 정삼각형
    Ellipse = 4      # 타원
    Circle = 5       # 원

# 도형 정의 클래스
class Figure:
    def __init__(self, ftype):
        self.figuretype = ftype
        self.startpoint = (0, 0)
        self.endpoint = (0, 0)
        self.radius = 0
        pass

    def width(self):
        return self.endpoint[0] - self.startpoint[0]

    def height(self):
        return self.endpoint[1] - self.startpoint[1]


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
        #self.screen.fill((0,0,0))


class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = parent.GetSize()
        self.size_dirty = True
        self.screen = None

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.parent.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 1.0
        self.timespacing = int(1000 / self.fps)
        #self.timer.Start(self.timespacing, False)

        self.linespacing = 5
        #window = pygame.display.set_mode(self.size)
        #self.thread = SDLThread(None)
        #self.thread.Start()

        self.figures = []
        self.currentfigure = None #Figure(FigureType.Rect)
        
        self.scalefactor = 1

    def update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.redraw()

    def redraw(self):
        #print("PyGame Redraw", self.size_dirty, self.size)
        if self.size_dirty:
            if self.screen is None:
                self.screen = pygame.Surface(self.size, 0, 32)
                self.screen.fill((240, 240, 240))
            else:
                oldscreen = self.screen.copy()
                self.screen = pygame.Surface(self.size, 0, 32)
                self.screen.fill((240, 240, 240))
                self.screen.blit(oldscreen, (0, 0))

            self.size_dirty = False
            #self.thread.setScreen(self.screen)

        self.screen.fill((240, 240, 240))
        cur = 0
        
        # pygame 그리기 예제
        #w, h = self.screen.get_size()
        #while cur <= h:
        #    pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))
        #    cur += self.linespacing
        #rect = pygame.Rect(random.randint(0, self.size[0]),
        #                   random.randint(0, self.size[1]), 100, 100)
        #pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # 도형 그리기
        for f in self.figures:
            if f.figuretype == FigureType.Rect:
                rect = pygame.Rect(f.startpoint[0], f.startpoint[1], f.width(), f.height())
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.Image(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.Bitmap(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self.parent)  # Device context for drawing the bitmap
        dc.SetUserScale(self.scalefactor, self.scalefactor)
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        print("scaled")
        del dc


    def OnPaint(self, event):
        self.redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.parent.GetSize()
        print("PyGame panel", self.size)
        self.size_dirty = True
        self.redraw()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        #self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)
        #self.thread.Stop()

    def mousedown(self, ftype, x, y):
        print("mouse down : ", (x, y))
        self.currentfigure = Figure(ftype)
        self.currentfigure.startpoint = (x, y)
        self.figures.append(self.currentfigure)        

    def mousedrag(self, x, y):
        self.currentfigure.endpoint = (x, y)
        self.redraw()

    def mouseup(self, x, y):
        if self.currentfigure is not None:
            self.currentfigure.endpoint = (x, y)
        self.currentfigure = None


class TabPanel1(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent, display):
        """"""
        wx.Panel.__init__(self, parent=parent)

        self.display = display

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))
        self.SetBackgroundColour("white")

        btn = wx.Button(self, label="Press Me Tab 1")

        self.Bind(wx.EVT_BUTTON, self.onClick, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    def onClick(self, event):
        self.display.redraw()
        pass

class TabPanel2(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent, display):
        """"""
        wx.Panel.__init__(self, parent=parent)

        self.display = display

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))
        self.SetBackgroundColour("white")

        btn = wx.Button(self, label="Press Me Tab 2")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.onClick, btn)

    def onClick(self, event):
        self.display.redraw()
        pass


class TabPanel3(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent, display):
        """"""
        wx.Panel.__init__(self, parent=parent)

        self.display = display

        colors = ["red", "blue", "gray", "yellow", "green"]
        #self.SetBackgroundColour(random.choice(colors))
        self.SetBackgroundColour("white")

        btn = wx.Button(self, label="Press Me Tab 3")
        btn.Bind(wx.EVT_BUTTON, self.onClick)
        
        self.scale_slider = wx.Slider(self, value=100, minValue=0, maxValue=500)
        self.scale_slider.Bind(wx.EVT_SCROLL, self.scale_changed)
        self.spinctrl = wx.SpinCtrl(self, min=0, max=500, initial=100)
        self.spinctrl.SetIncrement(10)
        self.spinctrl.Bind(wx.EVT_SPINCTRL, self.scalespinchanged)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        sizer.Add(self.scale_slider, 0, wx.ALL, 10)
        sizer.Add(self.spinctrl, 0, wx.ALL, 10)
        self.SetSizer(sizer)

    def onClick(self, event):
        print("btn")
        self.display.redraw()
        pass

    def scale_changed(self, event):
        scale = self.scale_slider.GetValue()
        self.display.scalefactor = round(scale / 100, 1)
        print("scale", self.display.scalefactor)
        self.spinctrl.SetValue(self.display.scalefactor * 100)
        self.display.redraw()

    def scalespinchanged(self, event):
        val = event.GetPosition()
        print("spin", val)
        self.display.scalefactor = round(val / 100, 1)
        self.display.redraw()


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, -1, title, size=(1024, 768))

        #wx.SystemOptions.SetOption("msw.notebook.themed-background", 0)
        #self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([-3, -4, -1, -2])
        self.statusbar.SetStatusText("Initializing...", 0)
        self.statusbar.SetStatusText("100:1", 2)

        # splitter and two main panel
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D, name="wxpython")
        self.splitter.SetMinimumPaneSize(200)

        self.panel1 = wx.Panel(self.splitter, -1)
        self.panel2 = wx.Panel(self.splitter, -1)
        self.splitter.SplitVertically(self.panel1, self.panel2, sashPosition=800)

        self.display = PygameDisplay(self.panel1, -1)
        self.panel1.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.panel1.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.panel1.Bind(wx.EVT_MOTION, self.OnDrag)

        # create tab on panel2
        notebook = wx.Notebook(self.panel2)
        tabOne = TabPanel1(notebook, self.display)
        notebook.AddPage(tabOne, "주차라인설정")
        tabTwo = TabPanel2(notebook, self.display)
        notebook.AddPage(tabTwo, "주차장설정")
        tabThree = TabPanel3(notebook, self.display)
        notebook.AddPage(tabThree, "공통설정")

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

        self.statusbar.SetStatusText("Initialized.", 0)

    def Kill(self, event):
        self.display.Kill(event)
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def Update(self, event):
        self.curframe += 1
        self.statusbar.SetStatusText("Frame %i" % self.curframe, 2)

    def OnScroll(self, event):
        self.display.linespacing = self.slider.GetValue()
        print("Scroll", event)

    def OnDown(self, event):
        x, y = event.GetPosition()
        print("Click coordinates: X=", x, " Y=", y)
        self.display.mousedown(FigureType.Rect, x, y)

    def OnUp(self, event):
        x, y = event.GetPosition()
        print("Release coordinates: X=", x, " Y=", y)
        self.display.mouseup(x, y)

    def OnDrag(self, event):
        x, y = event.GetPosition()
        if not event.Dragging():
            event.Skip()
            return
        event.Skip()
        # obj = event.GetEventObject()
        # sx, sy = obj.GetScreenPosition()
        # self.Move(sx+x,sy+y)
        print("Dragging position", x, y)
        self.display.mousedrag(x, y)

#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, id=-1, title='Parking Manager')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#---------------------------------------------------------------------------
pygame.init()
app = MyApp()
app.MainLoop()