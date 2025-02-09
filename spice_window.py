# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import spiceypy
import spiceypy.utils.support_types as stypes

METAKR = './mexMetaK.tm.txt'
START  = '2004 MAY 1 TDB'
STOP   = '2004 MAY 6 TDB'
TIMEFMT = "YYYY-MM-DDTHR:MN:SC.###::UTC"

def intersect(win1, win2):
    spiceypy.furnsh(METAKR)
    etbeg = spiceypy.str2et(START)
    etend = spiceypy.str2et(STOP)
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    # insert
    spiceypy.wninsd(etbeg, etend, cnfine)
    # intersect 同時可視
    win_int = spiceypy.wnintd(win1, win2)
    # 同時可視ウインドウの数
    winsiz = spiceypy.wncard(win_int)

    isbeg = []
    isend = []
    for i in range(winsiz):
        # fetch an interval
        [intbeg, intend] = spiceypy.wnfetd(win_int, i)
        btmstr = spiceypy.timout(intbeg, TIMEFMT)
        etmstr = spiceypy.timout(intend, TIMEFMT)
        dtbeg = dt.datetime.strptime(btmstr, "%Y-%m-%dT%H:%M:%S.%f")
        dtend = dt.datetime.strptime(etmstr, "%Y-%m-%dT%H:%M:%S.%f")
        isbeg.append(dtbeg)
        isend.append(dtend)
    spiceypy.unload(METAKR)
    return isbeg, isend


def invisible(win1, win2):
    spiceypy.furnsh(METAKR)
    etbeg = spiceypy.str2et(START)
    etend = spiceypy.str2et(STOP)
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    # insert
    spiceypy.wninsd(etbeg, etend, cnfine)
    # union 結合(どちらかが見えてるとき)
    win_uni = spiceypy.wnunid(win1, win2)
    # cnfineとdiff
    win_invisi = spiceypy.wndifd(cnfine, win_uni)
    # 不可視ウインドウの数
    winsiz = spiceypy.wncard(win_invisi)

    ivbeg = []
    ivend = []
    for i in range(winsiz):
        # fetch an interval
        [intbeg, intend] = spiceypy.wnfetd(win_invisi, i)
        btmstr = spiceypy.timout(intbeg, TIMEFMT)
        etmstr = spiceypy.timout(intend, TIMEFMT)
        dtbeg = dt.datetime.strptime(btmstr, "%Y-%m-%dT%H:%M:%S.%f")
        dtend = dt.datetime.strptime(etmstr, "%Y-%m-%dT%H:%M:%S.%f")
        ivbeg.append(dtbeg)
        ivend.append(dtend)
    spiceypy.unload(METAKR)
    return ivbeg, ivend


def plot(isbeg, isend, ivbeg, ivend):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for i in range(len(isbeg)):
        list_time = []
        list_visi = []
        list_time.append(isbeg[i])
        list_visi.append("simultaneous")
        list_time.append(isend[i])
        list_visi.append("simultaneous")
        ax1.plot(list_time, list_visi, c="b", marker=".")

    if len(ivbeg) == 0:
        # 不可視がない場合
        list_time = []
        list_visi = []
        # beg, endをプロット
    else:
        for i in range(len(ivbeg)):
            list_time = []
            list_visi = []
            list_time.append(ivbeg[i])
            list_visi.append("invisible")
            list_time.append(ivend[i])
            list_visi.append("invisible")
            ax1.plot(list_time, list_visi, c="b", marker=".")

    plt.show()
    return None


if __name__ == '__main__':
    spiceypy.furnsh(METAKR)
    etbeg1 = spiceypy.str2et('2004 MAY 2 TDB')
    etend1 = spiceypy.str2et('2004 MAY 4 TDB')
    win1 = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd(etbeg1, etend1, win1)
    etbeg2 = spiceypy.str2et('2004 MAY 3 TDB')
    etend2 = spiceypy.str2et('2004 MAY 5 TDB')
    win2 = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd(etbeg2, etend2, win2)
    spiceypy.unload(METAKR)

    isbeg, isend = intersect(win1, win2)
    ivbeg, ivend = invisible(win1, win2)
    plot(isbeg, isend, ivbeg, ivend)