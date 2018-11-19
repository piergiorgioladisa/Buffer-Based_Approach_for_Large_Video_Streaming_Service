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

# This controller is an implementation of the BBA0 Controller
# described in Chapter 4 of the paper:
# Zhi Li, et al, "A Buffer-Based Approach to Rate Adaptation: Evidence from a Large Video Streaming Service", Te-Yuan Huang, Ramesh Johari, Nick McKeown, Matthew Trunnell, Mark Watson Stanford University, Netflix

class BBA0Controller(BaseController):

    def __init__(self):
        super(BBA0Controller, self).__init__()

    def __repr__(self):
        return '<BBA0Controller-%d>' % id(self)

    def f(self, B_now):
        # The function f corresponds to the line equation between the points
        # (r,R_min) and (r+cu,R_max) when the value of Buf_now is
        # bounded by r and r+cu
        reservoir = self.feedback['max_buffer_time'] * 0.2
        cushion = self.feedback['max_buffer_time'] * 0.8 - reservoir * 0.5
        R_max = self.feedback['max_rate']
        R_min = self.feedback['min_rate']

        return B_now * ((R_max - R_min) / cushion) + (R_min - ((reservoir / cushion) * (R_max - R_min)))

    def maxR(self, constraint):
        Rates = self.feedback['rates']
        result = Rates[0]
        for i in Rates:
            if (i < constraint and result > i):
                result = i
        return result

    def minR(self, constraint):
        Rates = self.feedback['rates']
        result = Rates[0]
        for i in Rates:
            if (i > constraint and result < i):
                result = i
        return result

    def calcControlAction(self):

        # Retrive current iteration variables
        reservoir = self.feedback['max_buffer_time'] * 0.2
        cushion = self.feedback['max_buffer_time'] * 0.8 - reservoir * 0.5
        R_max = self.feedback['max_rate']
        R_min = self.feedback['min_rate']
        R_curr = self.feedback['cur_rate']
        B_now = self.feedback['queued_time']

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

        # Compute new rate based in current buffer region

        # Buffer in reservoir area
        if B_now <= reservoir:
            Rate_next = R_min

        # Buffer in upper reservoir area
        elif B_now >= reservoir + cushion:
            Rate_next = R_max

        # Buffer in cushion area
        elif self.f(B_now) >= R_plus:
            Rate_next = self.maxR(self.f(B_now))
        elif self.f(B_now) <= R_minus:
            Rate_next = self.minR(self.f(B_now))

        else:
            Rate_next = R_curr

        return Rate_next

