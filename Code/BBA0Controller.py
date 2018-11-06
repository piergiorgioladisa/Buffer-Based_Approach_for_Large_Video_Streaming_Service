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
    self.conf = {
        "r": 90,
        "cu": 126,
        "Rate_prev": 0.
    }

    def __repr__(self):
        return '<BBA0Controller-%d>' %id(self)

def calcControlAction(self):
    self.setIdleDuration(0.0)
    R_plus
    Rate_next
    B_now = self.feedback['queued_time']
    if self.conf["Rate_prev"] = self.feedback['max_rate']:
        R_plus = self.feedback['max_rate']
    else:
        R_plus = min{Ri > Rate_prev}
    if self.conf["Rate_prev"] = self.feedback['min_rate']:
        R_minus = self.feedback['min_rate']
    else:
        R_minus = max {Ri>Rate_prev}

    if self.feedback['queued_bytes'] <= self.conf["r"]:
        Rate_next= self.feedback['min_rate']
    else if self.feedback['queued_time'] >= self.conf["r"] + self.conf["cu"]:
        Rate_next =self.feedback['max_rate']
    function_res = f(self.feedback['queued_bytes'])
    else if function_res >= R_plus:
        Rate_next= max {Ri<function_res}
    else if function_res<= R_minus:
        Rate_next= min {Ri>function_res}
    else
        Rate_next=Rate_prev
    return Rate_next

def f(Buf_now):
    return (self.feedback['max_rate']-self.feedback['min_rate'])*self.feedback['queued_bytes']/(self.conf["r"] + self.conf["cu"])
                
