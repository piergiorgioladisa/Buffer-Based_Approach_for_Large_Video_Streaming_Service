#!/usr/bin/env python
# -*- Mode: Python -*-
# -*- encoding: utf-8 -*-
# Nicola Sebastianelli <nicola.sebastianelli.95@gmail.com>
# Piergiorgio Ladisa <piergiorgio.ladisa@hotmail.it>

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE" in the source distribution for more information.
import os, sys
from utils_py.util import debug, format_bytes
from BaseController import BaseController

DEBUG = 1
startup_phase = True

# This controller is an implementation of the BBA0 Controller
# described in Chapter 4 of the paper:
# Zhi Li, et al, "A Buffer-Based Approach to Rate Adaptation: Evidence from a Large Video Streaming Service",
# Te-Yuan Huang, Ramesh Johari, Nick McKeown, Matthew Trunnell, Mark Watson Stanford University, Netflix

class BBA2Controller(BaseController):

    def __init__(self):
        super(BBA2Controller, self).__init__()

    def __repr__(self):
        return '<BBA2Controller-%d>' % id(self)

    def f(self, B_now, reservoir, cushion, R_max, R_min):
        # The function f corresponds to the line equation between the points
        # (r,R_min) and (r+cu,R_max) when the value of Buf_now is
        # bounded by r and r+cu
        return B_now * ((R_max - R_min) / cushion) + (R_min - ((reservoir / cushion) * (R_max - R_min)))

    def maxR(self, constraint):
        Rates = self.feedback['rates']
        results = []
        for i in Rates:
            if (i < constraint):
                results.append(i)
        return max(results)

    def minR(self, constraint):
        Rates = self.feedback['rates']
        results = []
        for i in Rates:
            if (i > constraint):
                results.append(i)
        return min(results)

    def calcControlAction(self):

        # Retrive current iteration variables
        percentage_reservoir = 0.15
        percentage_cushion = 0.65
        percentage_upper_reservoir = 0.20
        reservoir = self.feedback['max_buffer_time'] * percentage_reservoir
        cushion = self.feedback['max_buffer_time'] * percentage_cushion
        R_max = self.feedback['max_rate']
        R_min = self.feedback['min_rate']
        R_curr = self.feedback['cur_rate']
        B_now = self.feedback['queued_time']
	delta_B = self.feedback['fragment_duration'] - (self.feedback['last_fragment_size'] / self.feedback['bwe'])
	global startup_phase	
	
        # Compute upperbound
        if R_curr == R_max:
            R_plus = R_max
        else:
            R_plus = self.minR(R_curr)

        # Compute lowerbound
        if R_curr == R_min:
            R_minus = R_min
        else:
            R_minus = self.maxR(R_curr)

        print "R_plus: ", R_plus
        print "R_minus: ", R_minus
        print "f(): ", self.f(B_now, reservoir, cushion, R_max, R_min)
	print "delta_B: ", delta_B
        # Compute new rate based in current buffer region
	
	
	if delta_B > (1- 0.5/(1.69*2)) * self.feedback['fragment_duration']:
	    Rate_next = R_plus
	
        # Buffer in reservoir area
        elif B_now <= reservoir:
            Rate_next = R_min

        # Buffer in upper reservoir area
        elif B_now >= reservoir + cushion:
            Rate_next = R_max

        # Buffer in cushion area
        elif self.f(B_now, reservoir, cushion, R_max, R_min) >= R_plus:
            Rate_next = self.maxR(self.f(B_now, reservoir, cushion, R_max, R_min))
            print "max f()"
        elif self.f(B_now, reservoir, cushion, R_max, R_min) <= R_minus:
            Rate_next = self.minR(self.f(B_now, reservoir, cushion, R_max, R_min))
            print "min f()"

        else:
            Rate_next = R_curr

        print "Reservoir: ", reservoir
        print "Cushion: ", cushion
        print "Upper_reservoir: ", self.feedback['max_buffer_time'] * percentage_upper_reservoir
        print "Rates: ", self.feedback['rates']
        print "R_max: ", R_max
        print "R_min: ", R_min
        print "R_curr: ", R_curr
        print "B_now: ", B_now

        return Rate_next

