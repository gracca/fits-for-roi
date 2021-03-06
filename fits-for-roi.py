#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#-----------------------------------------------------------------------#
# fits-for-roi.py                                                       #
#                                                                       #
# Script to create FITS files from ROI observing output                 #
# Copyright (C) 2013 Germán A. Racca - <gracca[AT]gmail[DOT]com>        #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#-----------------------------------------------------------------------#

import ast
import pyfits
import numpy as np

# read input file
f = open('d_110801.txt')
lines = f.readlines()

# define some variables
nheadlin = 22
nchannel = 2048
nspectra = len(lines) / nchannel
coef = nheadlin + nchannel + 1

# create a list of "empty" spectra (header + data)
spec = [pyfits.PrimaryHDU() for i in range(nspectra)]

# read numerical data
nums = np.zeros(nchannel*nspectra, dtype='float32')

for i in range(nspectra):
    limi = coef * i
    lims = limi + nheadlin
    nums[nchannel*i:nchannel*(i+1)] = lines[lims:lims+nchannel]

data = np.hsplit(nums, nspectra)

# read the headers
text = []

for i in range(nspectra):
    limi = coef * i
    lims = limi + nheadlin
    text.append(lines[limi:lims-1])

# format the headers
for i, j in enumerate(text):
    for m, k in enumerate(j):
        l = k.strip().replace("'", "").split("=")
        key = l[0].strip()
        val = l[1].strip()
        if m >= 4 and m <= 19:
            val = ast.literal_eval(val)
        spec[i].header.update(key, val)

# format the data
for i, j in enumerate(data):
    spec[i].data = j

# create fits files
name = 'd_110801'
for i in range(nspectra):
    n = name + '_' + str(i+1) + '.fits'
    spec[i].writeto(n, clobber=True)

