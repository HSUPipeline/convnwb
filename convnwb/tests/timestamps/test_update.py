"""Tests for convnwb.timestamps.update"""

import numpy as np

from convnwb.timestamps.update import *

###################################################################################################
###################################################################################################

def test_offset_time():

    times = np.array([1., 2., 3.])
    out = offset_time(times, 1.)
    expected = np.array([0., 1., 2.])
    assert np.array_equal(out, expected)

def test_change_time_units():

    times = np.array([1., 2., 3.])

    out1 = change_time_units(times, 10, 'divide')
    expected1 = np.array([0.1, 0.2, 0.3])
    assert np.array_equal(out1, expected1)

    out2 = change_time_units(times, 10, 'multiply')
    expected2 = np.array([10., 20., 30.])
    assert np.array_equal(out2, expected2)
