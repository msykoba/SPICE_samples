# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:24:03 2020

@author: masaya
"""

#
# Solution viewpr
#
# from __future__ import print_function
import numpy as np
import spiceypy
import spiceypy.utils.support_types as stypes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

iframe = 0
donothing = False  # switch to stop all recordering

def viewpr():
    #
    # Local Parameters
    #
    METAKR = './mexMetaK.tm.txt'
    TDBFMT = 'YYYY MON DD HR:MN:SC.### (TDB) ::TDB'
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL

    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh( METAKR )

    #
    # Assign the inputs for our search.
    #
    # Since we're interested in the apparent location of the
    # target, we use light time and stellar aberration
    # corrections. We use the "converged Newtonian" form
    # of the light time correction because this choice may
    # increase the accuracy of the occultation times we'll
    # compute using gfoclt.
    #
    srfpt  = 'DSS-14'
    obsfrm = 'DSS-14_TOPO'
    target = 'MEX'
    abcorr = 'CN+S'
    start  = '2004 MAY 2 TDB'
    stop   = '2004 MAY 6 TDB'
    elvlim =  6.0

    #
    # The elevation limit above has units of degrees; we convert
    # this value to radians for computation using SPICE routines.
    # We'll store the equivalent value in radians in revlim.
    #
    revlim = spiceypy.rpd() * elvlim

    #
    # Since SPICE doesn't directly support the AZ/EL coordinate
    # system, we use the equivalent constraint
    #
    #    latitude > revlim
    #
    # in the latitudinal coordinate system, where the reference
    # frame is topocentric and is centered at the viewing location.
    #
    crdsys = 'LATITUDINAL'
    coord  = 'LATITUDE'
    relate = '>'

    #
    # The adjustment value only applies to absolute extrema
    # searches; simply give it an initial value of zero
    # for this inequality search.
    #
    adjust = 0.0

    #
    # stepsz is the step size, measured in seconds, used to search
    # for times bracketing a state transition. Since we don't expect
    # any events of interest to be shorter than five minutes, and
    # since the separation between events is well over 5 minutes,
    # we'll use this value as our step size. Units are seconds.
    #
    stepsz = 300.0

    #
    # Display a banner for the output report:
    #
    print( '\n{:s}\n'.format(
           'Inputs for target visibility search:' )  )

    print( '   Target                       = '
           '{:s}'.format( target )  )
    print( '   Observation surface location = '
           '{:s}'.format( srfpt  )  )
    print( '   Observer\'s reference frame   = '
           '{:s}'.format( obsfrm )  )
    print( '   Elevation limit (degrees)    = '
           '{:f}'.format( elvlim )  )
    print( '   Aberration correction        = '
           '{:s}'.format( abcorr )  )
    print( '   Step size (seconds)          = '
           '{:f}'.format( stepsz )  )

    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et( start )
    etend = spiceypy.str2et( stop  )

    #
    # Display the search interval start and stop times
    # using the format shown below.
    #
    #    2004 MAY 06 20:15:00.000 (TDB)
    #
    timstr = spiceypy.timout( etbeg, TDBFMT )
    print( '   Start time                   = '
           '{:s}'.format(timstr) )

    timstr = spiceypy.timout( etend, TDBFMT )
    print( '   Stop time                    = '
           '{:s}'.format(timstr) )

    print( ' ' )

    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd( etbeg, etend, cnfine )

    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = stypes.SPICEDOUBLE_CELL( MAXWIN )

    #
    # Now search for the time period, within our confinement
    # window, during which the apparent target has elevation
    # at least equal to the elevation limit.
    #
    spiceypy.gfposc( target, obsfrm, abcorr, srfpt,
                     crdsys, coord,  relate, revlim,
                     adjust, stepsz, MAXIVL, cnfine, riswin )

    #
    # The function wncard returns the number of intervals
    # in a SPICE window.
    #
    winsiz = spiceypy.wncard( riswin )

    if winsiz == 0:

        print( 'No events were found.' )

    else:

        #
        # Display the visibility time periods.
        #
        print( 'Visibility times of {0:s} '
               'as seen from {1:s}:\n'.format(
                target, srfpt )                )

        for  i  in  range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            #
            [intbeg, intend] = spiceypy.wnfetd( riswin, i )

            #
            # Convert the rise time to a TDB calendar string.
            #
            timstr = spiceypy.timout( intbeg, TDBFMT )

            #
            # Write the string to standard output.
            #
            if  i  ==  0:

                print( 'Visibility or window start time:'
                       '  {:s}'.format( timstr )          )
            else:

                print( 'Visibility start time:          '
                       '  {:s}'.format( timstr )          )

            #
            # Convert the set time to a TDB calendar string.
            #
            timstr = spiceypy.timout( intend, TDBFMT )

            #
            # Write the string to standard output.
            #
            if  i  ==  (winsiz-1):

                print( 'Visibility or window stop time: '
                       '  {:s}'.format( timstr )          )
            else:

                print( 'Visibility stop time:           '
                       '  {:s}'.format( timstr )          )

            print( ' ' )

    spiceypy.unload( METAKR )


def visibl():
    #
    # Local Parameters
    #
    METAKR = './mexMetaK.tm.txt'
    TDBFMT = 'YYYY MON DD HR:MN:SC.### TDB ::TDB'
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL

    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh( METAKR )

    #
    # Assign the inputs for our search.
    #
    # Since we're interested in the apparent location of the
    # target, we use light time and stellar aberration
    # corrections. We use the "converged Newtonian" form
    # of the light time correction because this choice may
    # increase the accuracy of the occultation times we'll
    # compute using gfoclt.
    #
    srfpt  = 'DSS-14'
    obsfrm = 'DSS-14_TOPO'
    target = 'MEX'
    abcorr = 'CN+S'
    start  = '2004 MAY 2 TDB'
    stop   = '2004 MAY 6 TDB'
    elvlim =  6.0

    #
    # The elevation limit above has units of degrees; we convert
    # this value to radians for computation using SPICE routines.
    # We'll store the equivalent value in radians in revlim.
    #
    revlim = spiceypy.rpd() * elvlim

    #
    # We model the target shape as a point. We either model the
    # blocking body's shape as an ellipsoid, or we represent
    # its shape using actual topographic data. No body-fixed
    # reference frame is required for the target since its
    # orientation is not used.
    #
    back   = target
    bshape = 'POINT'
    bframe = ' '
    front  = 'MARS'
    fshape = 'ELLIPSOID'
    fframe = 'IAU_MARS'

    #
    # The occultation type should be set to 'ANY' for a point
    # target.
    #
    occtyp = 'any'

    #
    # Since SPICE doesn't directly support the AZ/EL coordinate
    # system, we use the equivalent constraint
    #
    #    latitude > revlim
    #
    # in the latitudinal coordinate system, where the reference
    # frame is topocentric and is centered at the viewing location.
    #
    crdsys = 'LATITUDINAL'
    coord  = 'LATITUDE'
    relate = '>'

    #
    # The adjustment value only applies to absolute extrema
    # searches; simply give it an initial value of zero
    # for this inequality search.
    #
    adjust = 0.0

    #
    # stepsz is the step size, measured in seconds, used to search
    # for times bracketing a state transition. Since we don't expect
    # any events of interest to be shorter than five minutes, and
    # since the separation between events is well over 5 minutes,
    # we'll use this value as our step size. Units are seconds.
    #
    stepsz = 300.0

    #
    # Display a banner for the output report:
    #
    print( '\n{:s}\n'.format(
           'Inputs for target visibility search:' )  )

    print( '   Target                       = '
           '{:s}'.format( target )  )
    print( '   Observation surface location = '
           '{:s}'.format( srfpt  )  )
    print( '   Observer\'s reference frame   = '
           '{:s}'.format( obsfrm )  )
    print( '   Blocking body                = '
           '{:s}'.format( front  )  )
    print( '   Blocker\'s reference frame    = '
           '{:s}'.format( fframe )  )
    print( '   Elevation limit (degrees)    = '
           '{:f}'.format( elvlim )  )
    print( '   Aberration correction        = '
           '{:s}'.format( abcorr )  )
    print( '   Step size (seconds)          = '
           '{:f}'.format( stepsz )  )

    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et( start )
    etend = spiceypy.str2et( stop  )

    #
    # Display the search interval start and stop times
    # using the format shown below.
    #
    #    2004 MAY 06 20:15:00.000 (TDB)
    #
    btmstr = spiceypy.timout( etbeg, TDBFMT )
    print( '   Start time                   = '
           '{:s}'.format(btmstr) )

    etmstr = spiceypy.timout( etend, TDBFMT )
    print( '   Stop time                    = '
           '{:s}'.format(etmstr) )

    print( ' ' )

    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd( etbeg, etend, cnfine )

    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = stypes.SPICEDOUBLE_CELL( MAXWIN )

    #
    # Now search for the time period, within our confinement
    # window, during which the apparent target has elevation
    # at least equal to the elevation limit.
    #
    spiceypy.gfposc( target, obsfrm, abcorr, srfpt,
                     crdsys, coord,  relate, revlim,
                     adjust, stepsz, MAXIVL, cnfine, riswin )

    #
    # Now find the times when the apparent target is above
    # the elevation limit and is not occulted by the
    # blocking body (Mars). We'll find the window of times when
    # the target is above the elevation limit and *is* occulted,
    # then subtract that window from the view period window
    # riswin found above.
    #
    # For this occultation search, we can use riswin as
    # the confinement window because we're not interested in
    # occultations that occur when the target is below the
    # elevation limit.
    #
    # Find occultations within the view period window.
    #
    print( ' Searching using ellipsoid target shape model...' )

    eocwin = stypes.SPICEDOUBLE_CELL( MAXWIN )

    fshape = 'ELLIPSOID'

    spiceypy.gfoclt( occtyp, front,  fshape,  fframe,
                     back,   bshape, bframe,  abcorr,
                     srfpt,  stepsz, riswin,  eocwin )
    print( ' Done.' )

    #
    # Subtract the occultation window from the view period
    # window: this yields the time periods when the target
    # is visible.
    #
    evswin = spiceypy.wndifd( riswin, eocwin )

    #
    #  Repeat the search using low-resolution DSK data
    # for the front body.
    #
    print( ' Searching using DSK target shape model...' )

    docwin = stypes.SPICEDOUBLE_CELL( MAXWIN )

    fshape = 'DSK/UNPRIORITIZED'

    spiceypy.gfoclt( occtyp, front,  fshape,  fframe,
                     back,   bshape, bframe,  abcorr,
                     srfpt,  stepsz, riswin,  docwin )
    print( ' Done.\n' )

    dvswin = spiceypy.wndifd( riswin, docwin )

    #
    # The function wncard returns the number of intervals
    # in a SPICE window.
    #
    winsiz = spiceypy.wncard( evswin )

    if winsiz == 0:

        print( 'No events were found.' )


    else:
        #
        # Display the visibility time periods.
        #
        print( 'Visibility start and stop times of '
               '{0:s} as seen from {1:s}\n'
               'using both ellipsoidal and DSK '
               'target shape models:\n'.format(
                   target, srfpt )                 )

        for  i  in  range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the ellipsoid
            # search result window evswin.
            #
            [intbeg, intend] = spiceypy.wnfetd( evswin, i )

            #
            # Convert the rise time to TDB calendar strings.
            # Write the results.
            #
            btmstr = spiceypy.timout( intbeg, TDBFMT )
            etmstr = spiceypy.timout( intend, TDBFMT )

            print( ' Ell: {:s} : {:s}'.format( btmstr, etmstr ) )

            #
            # Fetch the start and stop times of
            # the ith interval from the DSK
            # search result window dvswin.
            #
            [dintbg, dinten] = spiceypy.wnfetd( dvswin, i )

            #
            # Convert the rise time to TDB calendar strings.
            # Write the results.
            #
            btmstr = spiceypy.timout( dintbg, TDBFMT )
            etmstr = spiceypy.timout( dinten, TDBFMT )

            print( ' DSK: {:s} : {:s}\n'.format( btmstr, etmstr ) )
        #
        # End of result display loop.
        #

    spiceypy.unload( METAKR )


def shade():
    #
    # Local Parameters
    #
    METAKR = './mexMetaK.tm.txt'
    TDBFMT = 'YYYY MON DD HR:MN:SC.### TDB ::TDB'
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL

    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh( METAKR )
    
    #
    # input
    #
    front  = 'MARS'
    fshape = 'ELLIPSOID'
    fframe = 'IAU_MARS'
    ilusrc = 'SUN'
    back   = ilusrc
    bshape = 'ELLIPSOID'
    bframe = 'IAU_SUN'
    abcorr = 'CN+S'
    obssat = 'MEX'
    stepsz = 300.0
    umbra  = 'FULL'
    penumb = 'ANY'
    
    start  = '2004 MAY 2 TDB'
    stop   = '2004 MAY 6 TDB'
    
    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et( start )
    etend = spiceypy.str2et( stop  )
    btmstr = spiceypy.timout( etbeg, TDBFMT )
    print( '   Start time                   = '
           '{:s}'.format(btmstr) )
    etmstr = spiceypy.timout( etend, TDBFMT )
    print( '   Stop time                    = '
           '{:s}'.format(etmstr) )
    print( ' ' )
    
    #
    # Penumbra or Umbra
    #
    print( 'Searching using ellipsoid target shape model...' )
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd( etbeg, etend, cnfine )
    eocwin = stypes.SPICEDOUBLE_CELL( MAXWIN )
    spiceypy.gfoclt( penumb, front,  fshape,  fframe,
                     back,   bshape, bframe,  abcorr,
                     obssat, stepsz, cnfine,  eocwin )
    print( '\n{:s}\n'.format('Done.') )
    winsiz = spiceypy.wncard( eocwin )

    if winsiz == 0:
        print( 'No events were found.' )
    else:
        #
        # Display the visibility time periods.
        #
        print( 'Penumbra start and stop times of '
                '{0:s} as seen from {1:s}\n'
                'using ellipsoidal '
                'target shape models:\n'.format( obssat, ilusrc ))

        for  i  in  range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the ellipsoid
            # search result window evswin.
            #
            [intbeg, intend] = spiceypy.wnfetd( eocwin, i )

            #
            # Convert the rise time to TDB calendar strings.
            # Write the results.
            #
            btmstr = spiceypy.timout( intbeg, TDBFMT )
            etmstr = spiceypy.timout( intend, TDBFMT )

            print( ' Ell: {:s} : {:s}'.format( btmstr, etmstr ) )
    
    print( '\n{:s}\n'.format('Done.') )
    spiceypy.unload( METAKR )


def geometry_find():
    #
    # Local Parameters
    #
    METAKR = './mexMetaK.tm.txt'
    TDBFMT = 'YYYY MON DD HR:MN:SC.### (TDB) ::TDB'

    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh( METAKR )

    #
    # Inputs
    #
    target = 'MEX'
    frame  = 'IAU_MARS'
    abcorr = 'NONE'
    obsrvr = 'MARS'
    crdsys = 'LATITUDINAL'
    coord  = 'LATITUDE'
    relate = '<'
    lati   = 0.000000001
    refval = spiceypy.rpd() * lati
    adjust = 0.0
    step   = 300
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL

    start  = '2004 MAY 2 TDB'
    stop   = '2004 MAY 6 TDB'
    etbeg = spiceypy.str2et( start )
    etend = spiceypy.str2et( stop  )
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd( etbeg, etend, cnfine )
    riswin = stypes.SPICEDOUBLE_CELL( MAXWIN )

    spiceypy.gfposc( target, frame,  abcorr, obsrvr,
                     crdsys, coord,  relate, refval,
                     adjust, step,   MAXIVL, cnfine, riswin )
    winsiz = spiceypy.wncard( riswin )

    if winsiz == 0:

        print( 'No events were found.' )

    else:

        #
        # Display the visibility time periods.
        #
        print( 'Visibility times of {0:s} '
               'as seen from {1:s}:\n'.format(target, obsrvr) )

        for  i  in  range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            #
            [intbeg, intend] = spiceypy.wnfetd( riswin, i )

            #
            # Convert the rise time to a TDB calendar string.
            #
            timstr = spiceypy.timout( intbeg, TDBFMT )

            #
            # Write the string to standard output.
            #
            if  i  ==  0:

                print( 'Visibility or window start time:'
                       '  {:s}'.format( timstr )          )
            else:

                print( 'Visibility start time:          '
                       '  {:s}'.format( timstr )          )

            #
            # Convert the set time to a TDB calendar string.
            #
            timstr = spiceypy.timout( intend, TDBFMT )

            #
            # Write the string to standard output.
            #
            if  i  ==  (winsiz-1):

                print( 'Visibility or window stop time: '
                       '  {:s}'.format( timstr )          )
            else:

                print( 'Visibility stop time:           '
                       '  {:s}'.format( timstr )          )

            print( ' ' )

    spiceypy.unload( METAKR )


if __name__ == '__main__':
    # DSS-14から見たMEX可視
    viewpr()
    # DSS-14から見た火星による掩蔽を考慮したMEX可視
    visibl()
    # 日陰
    shade()
    # geometry finder
    geometry_find()