import numpy as np
import pandas as pd
from droppy.TimeDomain.TimeSignals import dx
from droppy.interpolate.dfInterpolate import interpolate



def slidingDamping( df , T ,  a, n = None ):
    """Compute equivalent damping from forced motion.

    Parameters
    ----------
    df : pd.Dataframe
        Forced motion results. should have "load" and "motion" columns, time is index
    T : float
        Period
    a : float
        Forced oscillation amplitude, if None, taken as max on each cycle.
    n : int
        Number of interpolation point per period. If None, closest to data, over 60 is used. Default is None

    Returns
    -------
    beq : pd.Series
        Equivalent damping function of time (sliding)
    """

    t = df.index
    w = 2 * np.pi / T

    if n is None :
        dt = dx( df )
        n = int(T/dt)
        n = max(n , 60)

    newTime = np.arange( min(t) , max(t) , T/(n)  )

    df_new = interpolate( df, newIndex = newTime  )

    beq = pd.Series( index = t[:-2*n] , dtype = float)

    for i in range( len(t) - 2*n ):
        mt = 0.5 * (df_new.load.values[i:i+n] + df_new.load.values[i+1:i+n+1] ) * np.diff( df_new.motion.iloc[i:i+n+1] )
        if a is None :
            a_ = df_new.motion.iloc[i:i+n+1].abs().max()
        else :
            a_ = a

        beq.values[i] = -np.sum(mt) / ( np.pi * a_**2 * w)

        # mt = moment_new.load.values[i:i+n+1] * moment_new.velocity.values[i:i+n+1]
        # beq2 = simps(mt , df.index[i:i+n+1] ) /  ( np.pi * a**2 * w)

    return beq



