# -*- coding: utf-8 -*-
"""
dynafig
Dynamic matplotlib in jupyer notebooks
Hans Buehler 2021
"""
import matplotlib.pyplot as plt
from IPython import display
from .logger import Logger
_log = Logger("Log")

class DeferredCall(object):
    """ Utility class which allows deferring a function call on an object
        Function can be access once execute() has been called
    """    

    class ResultHook(object):
        """ Allows deferred access to returns from the deferred function """
        def __init__(self, function):
            self._function  = function
            self._return    = []
            
        def __getattr__(self, key):
            _log.verify( len(self._return) == 1, "Deferred function '%s' has not yet been called for key '%s'", self._function, key )
            return getattr(self._return[0], key)
        
        def __call__(self):
            _log.verify( len(self._return) == 1, "Deferred function '%s' has not yet been called", self._function )
            return self._return[0]            
    
    def __init__(self, function : str, reduce_single_list : bool = True ):
        """ Initilize with the name 'function' of the function """
        self.function    = function
        self.red_list    = reduce_single_list
        self.kargs       = None
        self.kwargs      = None
        self.result_hook = None
    
    def __call__(self, *kargs, **kwargs ):
        """ Deferred function call. The returned hook can be used to read the result once execute() was called.
        """
        self.kargs       = kargs
        self.kwargs      = kwargs
        self.result_hook = DeferredCall.ResultHook(self.function)
        return self.result_hook

    def execute(self, owner):
        """ execute delayed function call and place result in function return b=hook """
        assert not self.kargs is None and not self.kwargs is None, "DreamCatcher for %s was never __call__ed" % self.function
        assert len(self.result_hook._return) == 0, "DreamCatcher for %s was already called" % self.function
        f = getattr(owner, self.function, None)
        _log.verify( not f is None, "Member function %s not found in object of type %s", self.function, owner.__class__.__name__ )
        r = f(*self.kargs, **self.kwargs)
        self.result_hook._return.append( r[0] if isinstance(r, list) and len(r) == 1 else r )
        
class DynamicAx(object):
    """ Wrapper around an matplotlib axis returned
        by DynamicFig, which is returned by figure().
    
        All calls to the returned axis are delegated to
        matplotlib with the amendmend that if any such function
        returs a list with one member, it will just return
        this member.
        This caters for the very common use case plot() where
        x,y are vectors. Assume y2 is an updated data set
        In this case we can use
        
            fig = figure()
            ax  = fig.add_subplot()
            lns = ax.plot( x, y, ":" )
            fig.render() # --> draw graph
            
            lns.set_ydata( y2 )
            fig.render() # --> change graph
    """
    
    def __init__(self, row : int, col : int ):
        """ Internal object which defers the creation of various graphics to a later point        
        """        
        self.row    = row
        self.col    = col
        self.plots  = {}
        self.caught = []
        self.ax     = None
    
    def initialize( self, fig, rows : int, cols : int):
        """ Creates the plot by calling all 'caught' functions calls in sequece """        
        assert self.ax is None, "Internal error; function called twice?"
        num     = 1 + self.col + self.row*cols
        self.ax = fig.add_subplot( rows, cols, num )        
        for catch in self.caught:
            catch.execute( self.ax )
            
    def __getattr__(self, key):
        if not self.ax is None:
            return getattr(self.ax, key)
        d = DeferredCall(key)
        self.caught.append(d)
        return d

class DynamicFig(object):
    
    def __init__(self, row_size : int = 5, col_size : int = 4, col_nums : int = 5):
        """ Setup object with a given output geometry
        
            Paraneters 
            ----------
                row_size : int, optional
                    Size for a row for matplot lib. Default is 5
                col_size : int, optional
                    Size for a column for matplot luib. Default is 4
                col_nums : int, optional
                    How many columns. Default is 5   
        """                
        self.hdisplay  = display.display("", display_id=True)
        self.axes      = []
        self.fig       = None
        self.row_size  = int(row_size)
        self.col_size  = int(col_size)
        self.col_nums  = int(col_nums)
        _log.verify( self.row_size > 0 and self.col_size > 0 and self.col_nums > 0, "Invalid input.")
        self.this_row  = 0
        self.this_col  = 0

    def add_subplot(self, new_row : bool = False) -> DynamicAx:
        """ Add a subplot
            This function will return a wrapper which defers the creation of the actual sub plot
            until all subplots were defined
            
            Parameters
            ----------
                new_row : bool, optional
                    Whether to force a new row. Default is False
            """            
        _log.verify( self.fig is None, "Cannot call add_subplot() after show() was called")
        if (self.this_col >= self.col_nums) or ( new_row and not self.this_col == 0 ):
            self.this_col = 0
            self.this_row = self.this_row + 1
        ax = DynamicAx( self.this_row, self.this_col )        
        self.axes.append(ax)
        self.this_col += 1
        return ax
    
    def render(self):
        """ Plot all axes.
            Once called, no further plots can be added, but the plots can
            be updated in place
        """
        if self.this_row == 0 and self.this_col == 0:
            return
        if self.fig is None:
            self.fig  = plt.figure( figsize = ( self.col_size*self.col_nums, self.row_size*(self.this_row+1)) )
            rows      = self.this_row+1
            cols      = self.col_nums
            for ax in self.axes:
                ax.initialize( self.fig, rows, cols )
            plt.close(self.fig)  # removes shaddow draw in Jupyter
        self.hdisplay.update(self.fig)  
    
def figure(row_size : int = 5, col_size : int = 4, col_nums : int = 5) -> DynamicFig:
    """ Generates a dynamic figure using matplot lib.
        It has the following main functions
        
            add_subplot():
                Used to create a sub plot. No need to provide the customary
                rows, cols, and total number as this will computed for you.
                
                All calls to the returned 'ax' are delegated to
                matplotlib with the amendmend that if any such function
                returs a list with one member, it will just return
                this member.
                This caters for the very common use case plot() where
                x,y are vectors. Assume y2 is an updated data set
                In this case we can use
                
                    fig = figure()
                    ax  = fig.add_subplot()
                    lns = ax.plot( x, y, ":" )
                    fig.render() # --> draw graph
                    
                    lns.set_ydata( y2 )
                    fig.render() # --> change graph
                    
            render():
                Draws the figure as it is.
                Call repeatedly if the underlying graphs are modified
                as per example above.
                No further add_subplots() are recommended

        Paraneters 
        ----------
            row_size : int, optional
                Size for a row for matplot lib. Default is 5
            col_size : int, optional
                Size for a column for matplot luib. Default is 4
            col_nums : int, optional
                How many columns. Default is 5  
                
        Returns
        -------
            DynamicFig
                A figure wrapper; see above.
    """   
    return DynamicFig( row_size=row_size, col_size=col_size, col_nums=col_nums ) 
    
    
def test():
    import numpy as np

    fig = DynamicFig()
    ax = fig.add_subplot()
    
    x = np.linspace(0,1,100)
    y = np.random.random(size=(100,1))
    
    ax.set_title("Hans")
    ax.set_xlim()
    l = ax.plot(x,y,":",color="red", label="hans")
    ax.legend()
    
    fig.render()
    
    import time
    for i in range(5):
        time.sleep(1)
        y = np.random.random(size=(100,1))
        l.set_ydata( y )
        fig.render()
        
