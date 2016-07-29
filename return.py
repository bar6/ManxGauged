#!/usr/bin/python

"""
Copyright (C) 2007 John Popplewell

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Contact : John Popplewell
Email   : john@johnnypops.demon.co.uk
Web     : http://www.johnnypops.demon.co.uk/python/

If you have any bug-fixes, enhancements or suggestions regarding this 
software, please contact me at the above email address.

$RCSfile: shapedclock.py,v $
$Id: shapedclock.py,v 1.2 2007/10/21 22:36:01 jfp Exp $
"""

import time
import math
import pygame 
#import py
import subprocess
import commands


from pygame.locals  import *
from wm_ext.appwnd import AppWnd

#from wmctrl import Window

#screen =pygame.display.set_mode((800, 480), 0, 32)

#lightbaroff = "lightbaroff.png"
#lightbaroff = pygame.image.load(lightbaroff).convert_alpha()
#lightbarrect = lightbaroff.get_rect()

#ps = subprocess.Popen(['wmctrl','-a','manxgauged'], stdout=subprocess.PIPE)


class ShapedClock(AppWnd):
    BACKGROUND_COLOUR   = (30, 62, 101)
    BORDER_COLOUR       = (0, 0, 0)
    TICK_COLOUR         = (0, 0, 0)
    HOUR_HAND_COLOUR    = (0, 0, 0)
    MINS_HAND_COLOUR    = (0, 0, 0)
    SECS_HAND_COLOUR    = (255, 0, 0)

    BORDER_WIDTH        = 0.05
    TICK_INSET          = 0.03
    SHORT_TICK_LEN      = 0.05
    LONG_TICK_LEN       = 0.09
    HAND_TIP_INSET      = 2
    POINT_LENGTH        = 0.083
    MINS_LENGTH         = 0.91
    HOUR_HAND_THICKNESS = 0.05
    MINS_HAND_THICKNESS = 0.05
    HAND_OVERHANG       = 0.05

    def __init__(self, x, y, size, preset, alwaysontop):
        opts = self.getDefaultOptions()
        opts.size = (size, size)
        opts.pos = (700, 25)
        opts.depth = 32
        opts.frame = 0
        opts.alwaysontop = 1
        self.move_start = None
        self.hours, self.mins, self.secs = -1, -1, -1
        AppWnd.__init__(self, opts)
        self.init("Return")
        self.doExpose()
        if preset is not None:
            self.SetPosition(preset)
        self._setShape()

    def _setShape(self):
        start = time.time()
        mask, transparent, solid = self.CreateDefaultShapeMask()
        size = self.screen_size
        center = size[0]/2, size[1]/2
        radius = center[0]
        pygame.draw.rect(mask, (0,0,255), (10,10,100,100))
        #pygame.draw.circle(mask, solid, center, radius)
        self.SetWindowShapeMask(mask)
        print "shape creation:", time.time()-start

    def SetPosition(self, preset):
        x, y = self.preset2pos(preset)
        self.SetWindowPosition((x, y))

    def _drawFace(self):
        size = self.screen_size
        center = size[0]/2, size[1]/2
        radius = center[0]
        self.screen.fill(self.BACKGROUND_COLOUR)
        #pygame.draw.circle(self.screen, self.BORDER_COLOUR, center, radius)
        #pygame.draw.circle(self.screen, self.BACKGROUND_COLOUR, center, int(radius*(1.0-self.BORDER_WIDTH)))
        angle, delta = -90.0, 360.0/12.0
        self.font = pygame.font.SysFont('Arial',25)
        self.screen.blit(self.font.render('Manx', True, (255,255,255)), (30,30))
        self.screen.blit(self.font.render('Gauged', True, (255,255,255)), (17,60))
        inset = radius*(self.TICK_INSET + self.BORDER_WIDTH)
        s_r_end = radius - inset
        s_r_start = s_r_end - self.SHORT_TICK_LEN*radius
        l_r_start = s_r_end - self.LONG_TICK_LEN*radius
        for i in range(12):
            theta = math.radians(angle)
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            if i % 3:
                start = (center[0] + s_r_start*cos_theta, center[1] + s_r_start*sin_theta)
            else:
                start = (center[0] + l_r_start*cos_theta, center[1] + l_r_start*sin_theta)
            end = (center[0] + s_r_end*cos_theta, center[1] + s_r_end*sin_theta)
            #pygame.draw.aaline(self.screen, self.TICK_COLOUR, start, end)
            angle += delta

    def _transformHand(self, origin, points, angle):
        theta = math.radians(-90.0 + angle)
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        tp = []
        ox, oy = origin
        for point in points:
            x, y = point
            nx = ox + (x*cos_theta - y*sin_theta)
            ny = oy + (y*cos_theta + x*sin_theta)
            tp.append((nx, ny))
        return tp

    def _drawHands(self, hours, mins, secs):
        size = self.screen_size
        center = size[0]/2, size[1]/2
        radius = center[0]
        inset = radius*(self.TICK_INSET + self.BORDER_WIDTH)
        length = radius - inset - radius*self.LONG_TICK_LEN - self.HAND_TIP_INSET
        mins_length = self.MINS_LENGTH*length
        overhang = radius*self.HAND_OVERHANG
        # clear background
        pygame.draw.circle(self.screen, self.BACKGROUND_COLOUR, center, int(length+2))
        # draw hour-hand
        w = radius*self.HOUR_HAND_THICKNESS/2.0
        r = mins_length/1.61803399
        p = self.POINT_LENGTH*length
        points =((-overhang, 0), (0, -w), (r-p, -w), (r, 0), (r-p, w), (0, w))
        angle = (360.0/12.0)*((hours % 12) + (mins/60.0))
        t_points = self._transformHand(center, points, angle)
        pygame.draw.aalines(self.screen, self.HOUR_HAND_COLOUR, 1, t_points, 1)
        # draw minute-hand
        w = radius*self.MINS_HAND_THICKNESS/2.0
        r = mins_length
        p = self.POINT_LENGTH*length
        points =((-overhang, 0), (0, -w), (r-p, -w), (r, 0), (r-p, w), (0, w))
        angle = (360.0/60.0)*(mins + (secs/60.0))
        t_points = self._transformHand(center, points, angle)
        pygame.draw.aalines(self.screen, self.MINS_HAND_COLOUR, 1, t_points, 1)
        # draw seconds-hand
        r = length-2
        points =((-2*overhang, 0), (r, 0))
        angle = (360.0/60.0)*secs
        t_points = self._transformHand(center, points, angle)
        pygame.draw.aalines(self.screen, self.SECS_HAND_COLOUR, 0, t_points, 1)

    def _refreshHands(self):
        _, _, _, hours, mins, secs, _, _, _ = time.localtime()
        self._drawHands(hours, mins, secs)

    def doExpose(self):
        self._drawFace()
        #self._refreshHands()
        #pygame.display.flip()

    def doResize(self, size):
        self.doExpose()

    def doEvent(self, event):
        if event.type in (KEYUP, KEYDOWN):
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                     return 1
                elif event.key >= K_KP1 and event.key <= K_KP9:
                    self.SetPosition(event.key-K_KP1+1)
        elif event.type == MOUSEBUTTONDOWN:
            if not self.IsMaximized() and event.button == 1:
                self.move_start = self.Client2Screen(event.pos)
                self.move_orig  = self.GetWindowPosition()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.move_start = None
                ps = subprocess.Popen(['wmctrl','-a','manxgauged'], stdout=subprocess.PIPE)
        elif event.type == MOUSEMOTION:
            if self.move_start:
                pos = self.Client2Screen(event.pos)
                x = self.move_orig[0] + (pos[0] - self.move_start[0])
                y = self.move_orig[1] + (pos[1] - self.move_start[1])
                self.SetWindowPosition((x, y))
        return 0

    def doRun(self):
        _, _, _, hours, mins, secs, _, _, _ = time.localtime()
        if self.hours != hours or self.mins != mins or self.secs != secs:
            #self.hours, self.mins, self.secs = hours, mins, secs
            #self._drawHands(hours, mins, secs)
            pygame.display.flip()
        pygame.time.wait(1)

    def go(self):
        self.run()
        self.quit()


from optparse import OptionParser, OptionValueError

if __name__ == "__main__":
    def int_rangeCB(option, opt_str, value, parser, lower, upper):
        if value < lower or value > upper:
            raise OptionValueError("option %s: integer value out of range [%d-%d]."%(opt_str, lower, upper))
        setattr(parser.values, option.dest, value)

    parser = OptionParser()
    parser.add_option("-s", "--size", default=200, action="callback", callback=int_rangeCB, callback_args=(100, 1024), dest="size", metavar="SIZE", type="int", help="set clock size in pixels [default: %default]")
    parser.add_option("-x", "--x", default=-1, dest="x", metavar="X", type="int", help="set window left X")
    parser.add_option("-y", "--y", default=-1, dest="y", metavar="Y", type="int", help="set window top  Y")
    parser.add_option("-p", "--preset", action="callback", callback=int_rangeCB, callback_args=(1, 9), dest="pos", metavar="POS", type="int", help="position window in one of 9 preset locations")
    parser.add_option("--alwaysontop",action="store_true", dest="alwaysontop", default=False, help="keep window on top of others")
    opts, args = parser.parse_args()
    app = ShapedClock(opts.x, opts.y, opts.size, opts.pos, opts.alwaysontop)
    app.go()

