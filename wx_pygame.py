### PYGAME IN WX ###
# A simple test of embedding Pygame in a wxPython frame
#
# By David Barker (aka Animatinator), 14/07/2010
# Patch for cross-platform support by Sean McKean, 16/07/2010
# Patch to fix redrawing issue by David Barker, 20/07/2010
# Second window demo added by David Barker, 21/07/2010

# modified by Yuxi Luo (Skycocoo), 19/06/2018
# removed all deprecated methods to current pygame & wx version
# pygame == 1.9.3
# wxpython == 4.0.1


import wx, sys, os, pygame

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = self.GetSize()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 60.0
        self.timespacing = int(1000.0 / self.fps)
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        self.screen.fill((0,0,0))

        cur = 0

        w, h = self.screen.get_size()
        while cur <= h:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))

            cur += self.linespacing

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.Image(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.Bitmap(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.GetSize()
        self.size_dirty = True

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)


class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (600, 600))

        self.display = PygameDisplay(self, -1)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("wxPython", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

        self.curframe = 0

        self.SetTitle("Pygame embedded in wxPython")

        self.slider = wx.Slider(self, wx.ID_ANY, 5, 1, 10, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider.SetTickFreq(1)
        self.button = wx.Button(self, -1, "DO NOT PRESS THIS BUTTON")

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.button)

        self.timer.Start(int(1000 / self.display.fps))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.slider, 1, flag = wx.EXPAND | wx.RIGHT, border = 5)
        self.sizer2.Add(self.button, 0, flag = wx.EXPAND | wx.ALL, border = 5)
        self.sizer.Add(self.sizer2, 0, flag = wx.EXPAND)
        self.sizer.Add(self.display, 1, flag = wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

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

    def ButtonClick(self, event):
        # (Commented code replaces the main display with the 'foooool!' display)
        #self.sizer.Detach(self.display)
        #self.display.Destroy()
        #self.display = FoolDisplay(self, -1)
        #self.sizer.Add(self.display, 1, flag = wx.EXPAND)
        #self.Layout()

        #newframe = FoolFrame(self)
        #newframe.Show()

        self.button.SetLabel("YOU WERE WARNED!")
        self.Layout()

class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)

        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()