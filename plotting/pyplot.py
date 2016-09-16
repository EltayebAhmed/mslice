# This file was created from matplotlib.pyplot
# matplotlib version 1.5.2
from figuremanager import FigureManager,activate_category
from script_generation import script_log
from _pyplot_decorators import draw_colorbar

#imports from matplotlit.pyplot
from matplotlib.cbook import dedent, silent_list, is_string_like, is_numlike
import matplotlib
from matplotlib import docstring
from matplotlib.axes import Axes, Subplot
from matplotlib.figure import Figure, figaspect
from matplotlib.gridspec import GridSpec
from matplotlib.artist import setp as _setp
from matplotlib.cbook import _string_to_bool
from matplotlib.projections import PolarAxes

from matplotlib import cm
from matplotlib import mlab
from matplotlib.image import imread as _imread
from matplotlib.image import imsave as _imsave
from matplotlib.externals import six
import six
import sys

import warnings
import numpy as np

module_name = "cli"  # This is passed to who ever is managing the script logging
                     # This will be the name of the module in the script



# These are functions that exist is in matplotlib.pyplot but have been redefined.
def figure(num=None):
    return FigureManager.get_figure_number(num).get_figure()


def gcf():
    return FigureManager.get_active_figure().get_figure()


def draw_if_interactive():
    # We will always draw because mslice might be running without matplotlib interactive
    for fig in FigureManager.all_figures():
        fig.canvas.draw()


def draw_all():
    for fig in FigureManager.all_figures():
        fig.canvas.draw_idle()

# All functions in this file have been copied over from matplotlib.pyplot  exactly as defined except the functions
# defined before  this comment.

# The following tuple is a list of all the functions in matplotlib.pyplot that have NOT been included in this interface
___unincluded_functions = ('_backend_selection',
                           'install_repl_displayhook',
                           'uninstall_repl_displayhook',
                           'switch_backend',
                           'show',
                           'ioff',
                           'pause',
                           'xkcd',
                           '_auto_draw_if_interactive',
                           'fignum_exists',
                           'get_fignums',
                           'get_fignums',
                           'get_figlabels',
                           'get_current_fig_manager',
                           'connect',
                           'disconnect',
                           'close',
						   'draw',
						   'subplot_tool',
						   'get_plot_commands',
						   '<all_colormap_setting_functions>'
                           )


def get_unincluded_functions():
    return ___unincluded_functions


__redefined_functions = ('figure',
                         'gcf',
                         'draw_if_interactive',
                         'draw_all'
)


def get_redefined_functions():
    return __redefined_functions
# These are functions that have been copied over from matplotlib.pyplot exactly as defined, decorators are added as
# appropriate

_IP_REGISTERED = None
_INSTALL_FIG_OBSERVER = False
def install_repl_displayhook():
    """
    Install a repl display hook so that any stale figure are automatically
    redrawn when control is returned to the repl.

    This works with both IPython terminals and vanilla python shells.
    """
    global _IP_REGISTERED
    global _INSTALL_FIG_OBSERVER

    class _NotIPython(Exception):
        pass

    # see if we have IPython hooks around, if use them

    try:
        if 'IPython' in sys.modules:
            from IPython import get_ipython
            ip = get_ipython()
            if ip is None:
                raise _NotIPython()

            if _IP_REGISTERED:
                return

            def post_execute():
                if matplotlib.is_interactive():
                    draw_all()

            # IPython >= 2
            try:
                ip.events.register('post_execute', post_execute)
            except AttributeError:
                # IPython 1.x
                ip.register_post_execute(post_execute)

            _IP_REGISTERED = post_execute
            _INSTALL_FIG_OBSERVER = False
        else:
            _INSTALL_FIG_OBSERVER = True

    # import failed or ipython is not running
    except (ImportError, _NotIPython):
        _INSTALL_FIG_OBSERVER = True
install_repl_displayhook()

def findobj(o=None, match=None, include_self=True):
    if o is None:
        o = gcf()
    return o.findobj(match, include_self=include_self)


def isinteractive():
    """
    Return status of interactive mode.
    """
    return matplotlib.is_interactive()


@docstring.copy_dedent(matplotlib.rc)
def rc(*args, **kwargs):
    matplotlib.rc(*args, **kwargs)


@docstring.copy_dedent(matplotlib.rc_context)
def rc_context(rc=None, fname=None):
    return matplotlib.rc_context(rc, fname)


@docstring.copy_dedent(matplotlib.rcdefaults)
def rcdefaults():
    matplotlib.rcdefaults()
    if matplotlib.is_interactive():
        draw_all()

def gci():
    """
    Get the current colorable artist.  Specifically, returns the
    current :class:`~matplotlib.cm.ScalarMappable` instance (image or
    patch collection), or *None* if no images or patch collections
    have been defined.  The commands :func:`~matplotlib.pyplot.imshow`
    and :func:`~matplotlib.pyplot.figimage` create
    :class:`~matplotlib.image.Image` instances, and the commands
    :func:`~matplotlib.pyplot.pcolor` and
    :func:`~matplotlib.pyplot.scatter` create
    :class:`~matplotlib.collections.Collection` instances.  The
    current image is an attribute of the current axes, or the nearest
    earlier axes in the current figure that contains an image.
    """
    return gcf()._gci()


def sci(im):
    """
    Set the current image.  This image will be the target of colormap
    commands like :func:`~matplotlib.pyplot.jet`,
    :func:`~matplotlib.pyplot.hot` or
    :func:`~matplotlib.pyplot.clim`).  The current image is an
    attribute of the current axes.
    """
    gca()._sci(im)


def setp(*args, **kwargs):
    return _setp(*args, **kwargs)


@script_log(module_name)
def clf():
    """
    Clear the current figure.
    """
    gcf().clf()


@docstring.copy_dedent(Figure.savefig)
def savefig(*args, **kwargs):
    fig = gcf()
    res = fig.savefig(*args, **kwargs)
    fig.canvas.draw_idle()   # need this if 'transparent=True' to reset colors
    return res


@docstring.copy_dedent(Figure.ginput)
def ginput(*args, **kwargs):
    """
    Blocking call to interact with the figure.

    This will wait for *n* clicks from the user and return a list of the
    coordinates of each click.

    If *timeout* is negative, does not timeout.
    """
    return gcf().ginput(*args, **kwargs)


@docstring.copy_dedent(Figure.waitforbuttonpress)
def waitforbuttonpress(*args, **kwargs):
    """
    Blocking call to interact with the figure.

    This will wait for *n* key or mouse clicks from the user and
    return a list containing True's for keyboard clicks and False's
    for mouse clicks.

    If *timeout* is negative, does not timeout.
    """
    return gcf().waitforbuttonpress(*args, **kwargs)

@script_log(module_name)
@docstring.copy_dedent(Figure.text)
def figtext(*args, **kwargs):
    return gcf().text(*args, **kwargs)


# scriptlog everything from now onwards ...............................
@docstring.copy_dedent(Figure.suptitle)
def suptitle(*args, **kwargs):
    return gcf().suptitle(*args, **kwargs)


@docstring.Appender("Addition kwargs: hold = [True|False] overrides default hold state", "\n")
@docstring.copy_dedent(Figure.figimage)
def figimage(*args, **kwargs):
    # allow callers to override the hold state by passing hold=True|False
    #sci(ret)  # JDH figimage should not set current image -- it is not mappable, etc
    return gcf().figimage(*args, **kwargs)

@script_log(module_name)
def figlegend(handles, labels, loc, **kwargs):
    """
    Place a legend in the figure.

    *labels*
      a sequence of strings

    *handles*
      a sequence of :class:`~matplotlib.lines.Line2D` or
      :class:`~matplotlib.patches.Patch` instances

    *loc*
      can be a string or an integer specifying the legend
      location

    A :class:`matplotlib.legend.Legend` instance is returned.

    Example::

      figlegend( (line1, line2, line3),
                 ('label1', 'label2', 'label3'),
                 'upper right' )

    .. seealso::

       :func:`~matplotlib.pyplot.legend`

    """
    return gcf().legend(handles, labels, loc, **kwargs)


@script_log(module_name)
def hold(b=None):
    """
    Set the hold state.  If *b* is None (default), toggle the
    hold state, else set the hold state to boolean value *b*::

      hold()      # toggle hold
      hold(True)  # hold is on
      hold(False) # hold is off

    When *hold* is *True*, subsequent plot commands will be added to
    the current axes.  When *hold* is *False*, the current axes and
    figure will be cleared on the next plot command.
    """

    fig = gcf()
    ax = fig.gca()

    fig.hold(b)
    ax.hold(b)

    # b=None toggles the hold state, so let's get get the current hold
    # state; but should pyplot hold toggle the rc setting - me thinks
    # not
    b = ax.ishold()

    rc('axes', hold=b)


def ishold():
    """
    Return the hold status of the current axes.
    """
    return gca().ishold()



def over(func, *args, **kwargs):
    """
    Call a function with hold(True).

    Calls::

      func(*args, **kwargs)

    with ``hold(True)`` and then restores the hold state.
    """
    h = ishold()
    hold(True)
    func(*args, **kwargs)
    hold(h)


@script_log(module_name)
def axes(*args, **kwargs):
    """
    Add an axes to the figure.

    The axes is added at position *rect* specified by:

    - ``axes()`` by itself creates a default full ``subplot(111)`` window axis.

    - ``axes(rect, axisbg='w')`` where *rect* = [left, bottom, width,
      height] in normalized (0, 1) units.  *axisbg* is the background
      color for the axis, default white.

    - ``axes(h)`` where *h* is an axes instance makes *h* the current
      axis.  An :class:`~matplotlib.axes.Axes` instance is returned.

    =======   ==============   ==============================================
    kwarg     Accepts          Description
    =======   ==============   ==============================================
    axisbg    color            the axes background color
    frameon   [True|False]     display the frame?
    sharex    otherax          current axes shares xaxis attribute
                               with otherax
    sharey    otherax          current axes shares yaxis attribute
                               with otherax
    polar     [True|False]     use a polar axes?
    aspect    [str | num]      ['equal', 'auto'] or a number.  If a number
                               the ratio of x-unit/y-unit in screen-space.
                               Also see
                               :meth:`~matplotlib.axes.Axes.set_aspect`.
    =======   ==============   ==============================================

    Examples:

    * :file:`examples/pylab_examples/axes_demo.py` places custom axes.
    * :file:`examples/pylab_examples/shared_axis_demo.py` uses
      *sharex* and *sharey*.

    """

    nargs = len(args)
    if len(args) == 0:
        return subplot(111, **kwargs)
    if nargs > 1:
        raise TypeError('Only one non keyword arg to axes allowed')
    arg = args[0]

    if isinstance(arg, Axes):
        a = gcf().sca(arg)
    else:
        rect = arg
        a = gcf().add_axes(rect, **kwargs)
    return a


@script_log(module_name)
def delaxes(*args):
    """
    Remove an axes from the current figure.  If *ax*
    doesn't exist, an error will be raised.

    ``delaxes()``: delete the current axes
    """
    if not len(args):
        ax = gca()
    else:
        ax = args[0]
    ret = gcf().delaxes(ax)
    return ret


def gca(**kwargs):
    """
    Get the current :class:`~matplotlib.axes.Axes` instance on the
    current figure matching the given keyword args, or create one.

    Examples
    ---------
    To get the current polar axes on the current figure::

        plt.gca(projection='polar')

    If the current axes doesn't exist, or isn't a polar one, the appropriate
    axes will be created and then returned.

    See Also
    --------
    matplotlib.figure.Figure.gca : The figure's gca method.
    """
    return gcf().gca(**kwargs)


def subplot(*args, **kwargs):
    """
    Return a subplot axes positioned by the given grid definition.

    Typical call signature::

      subplot(nrows, ncols, plot_number)

    Where *nrows* and *ncols* are used to notionally split the figure
    into ``nrows * ncols`` sub-axes, and *plot_number* is used to identify
    the particular subplot that this function is to create within the notional
    grid. *plot_number* starts at 1, increments across rows first and has a
    maximum of ``nrows * ncols``.

    In the case when *nrows*, *ncols* and *plot_number* are all less than 10,
    a convenience exists, such that the a 3 digit number can be given instead,
    where the hundreds represent *nrows*, the tens represent *ncols* and the
    units represent *plot_number*. For instance::

      subplot(211)

    produces a subaxes in a figure which represents the top plot (i.e. the
    first) in a 2 row by 1 column notional grid (no grid actually exists,
    but conceptually this is how the returned subplot has been positioned).

    .. note::

       Creating a new subplot with a position which is entirely inside a
       pre-existing axes will trigger the larger axes to be deleted::

          import matplotlib.pyplot as plt
          # plot a line, implicitly creating a subplot(111)
          plt.plot([1,2,3])
          # now create a subplot which represents the top plot of a grid
          # with 2 rows and 1 column. Since this subplot will overlap the
          # first, the plot (and its axes) previously created, will be removed
          plt.subplot(211)
          plt.plot(range(12))
          plt.subplot(212, axisbg='y') # creates 2nd subplot with yellow background

       If you do not want this behavior, use the
       :meth:`~matplotlib.figure.Figure.add_subplot` method or the
       :func:`~matplotlib.pyplot.axes` function instead.

    Keyword arguments:

      *axisbg*:
        The background color of the subplot, which can be any valid
        color specifier.  See :mod:`matplotlib.colors` for more
        information.

      *polar*:
        A boolean flag indicating whether the subplot plot should be
        a polar projection.  Defaults to *False*.

      *projection*:
        A string giving the name of a custom projection to be used
        for the subplot. This projection must have been previously
        registered. See :mod:`matplotlib.projections`.

    .. seealso::

        :func:`~matplotlib.pyplot.axes`
            For additional information on :func:`axes` and
            :func:`subplot` keyword arguments.

        :file:`examples/pie_and_polar_charts/polar_scatter_demo.py`
            For an example

    **Example:**

    .. plot:: mpl_examples/subplots_axes_and_figures/subplot_demo.py

    """
    # if subplot called without arguments, create subplot(1,1,1)
    if len(args)==0:
        args=(1,1,1)

    # This check was added because it is very easy to type
    # subplot(1, 2, False) when subplots(1, 2, False) was intended
    # (sharex=False, that is). In most cases, no error will
    # ever occur, but mysterious behavior can result because what was
    # intended to be the sharex argument is instead treated as a
    # subplot index for subplot()
    if len(args) >= 3 and isinstance(args[2], bool) :
        warnings.warn("The subplot index argument to subplot() appears"
                      " to be a boolean. Did you intend to use subplots()?")

    fig = gcf()
    a = fig.add_subplot(*args, **kwargs)
    bbox = a.bbox
    byebye = []
    for other in fig.axes:
        if other==a: continue
        if bbox.fully_overlaps(other.bbox):
            byebye.append(other)
    for ax in byebye: delaxes(ax)

    return a


@script_log(module_name)
def subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                subplot_kw=None, gridspec_kw=None, **fig_kw):
    """
    Create a figure with a set of subplots already made.

    This utility wrapper makes it convenient to create common layouts of
    subplots, including the enclosing figure object, in a single call.

    Keyword arguments:

      *nrows* : int
        Number of rows of the subplot grid.  Defaults to 1.

      *ncols* : int
        Number of columns of the subplot grid.  Defaults to 1.

      *sharex* : string or bool
        If *True*, the X axis will be shared amongst all subplots.  If
        *True* and you have multiple rows, the x tick labels on all but
        the last row of plots will have visible set to *False*
        If a string must be one of "row", "col", "all", or "none".
        "all" has the same effect as *True*, "none" has the same effect
        as *False*.
        If "row", each subplot row will share a X axis.
        If "col", each subplot column will share a X axis and the x tick
        labels on all but the last row will have visible set to *False*.

      *sharey* : string or bool
        If *True*, the Y axis will be shared amongst all subplots. If
        *True* and you have multiple columns, the y tick labels on all but
        the first column of plots will have visible set to *False*
        If a string must be one of "row", "col", "all", or "none".
        "all" has the same effect as *True*, "none" has the same effect
        as *False*.
        If "row", each subplot row will share a Y axis and the y tick
        labels on all but the first column will have visible set to *False*.
        If "col", each subplot column will share a Y axis.

      *squeeze* : bool
        If *True*, extra dimensions are squeezed out from the
        returned axis object:

        - if only one subplot is constructed (nrows=ncols=1), the
          resulting single Axis object is returned as a scalar.

        - for Nx1 or 1xN subplots, the returned object is a 1-d numpy
          object array of Axis objects are returned as numpy 1-d
          arrays.

        - for NxM subplots with N>1 and M>1 are returned as a 2d
          array.

        If *False*, no squeezing at all is done: the returned axis
        object is always a 2-d array containing Axis instances, even if it
        ends up being 1x1.

      *subplot_kw* : dict
        Dict with keywords passed to the
        :meth:`~matplotlib.figure.Figure.add_subplot` call used to
        create each subplots.

      *gridspec_kw* : dict
        Dict with keywords passed to the
        :class:`~matplotlib.gridspec.GridSpec` constructor used to create
        the grid the subplots are placed on.

      *fig_kw* : dict
        Dict with keywords passed to the :func:`figure` call.  Note that all
        keywords not recognized above will be automatically included here.

    Returns:

    fig, ax : tuple

      - *fig* is the :class:`matplotlib.figure.Figure` object

      - *ax* can be either a single axis object or an array of axis
        objects if more than one subplot was created.  The dimensions
        of the resulting array can be controlled with the squeeze
        keyword, see above.

    Examples::

        x = np.linspace(0, 2*np.pi, 400)
        y = np.sin(x**2)

        # Just a figure and one subplot
        f, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title('Simple plot')

        # Two subplots, unpack the output array immediately
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.plot(x, y)
        ax1.set_title('Sharing Y axis')
        ax2.scatter(x, y)

        # Four polar axes
        plt.subplots(2, 2, subplot_kw=dict(polar=True))

        # Share a X axis with each column of subplots
        plt.subplots(2, 2, sharex='col')

        # Share a Y axis with each row of subplots
        plt.subplots(2, 2, sharey='row')

        # Share a X and Y axis with all subplots
        plt.subplots(2, 2, sharex='all', sharey='all')
        # same as
        plt.subplots(2, 2, sharex=True, sharey=True)
    """
    # for backwards compatibility
    if isinstance(sharex, bool):
        if sharex:
            sharex = "all"
        else:
            sharex = "none"
    if isinstance(sharey, bool):
        if sharey:
            sharey = "all"
        else:
            sharey = "none"
    share_values = ["all", "row", "col", "none"]
    if sharex not in share_values:
        # This check was added because it is very easy to type
        # `subplots(1, 2, 1)` when `subplot(1, 2, 1)` was intended.
        # In most cases, no error will ever occur, but mysterious behavior will
        # result because what was intended to be the subplot index is instead
        # treated as a bool for sharex.
        if isinstance(sharex, int):
            warnings.warn("sharex argument to subplots() was an integer."
                          " Did you intend to use subplot() (without 's')?")

        raise ValueError("sharex [%s] must be one of %s" %
                         (sharex, share_values))
    if sharey not in share_values:
        raise ValueError("sharey [%s] must be one of %s" %
                         (sharey, share_values))
    if subplot_kw is None:
        subplot_kw = {}
    if gridspec_kw is None:
        gridspec_kw = {}

    fig = figure(**fig_kw)
    gs = GridSpec(nrows, ncols, **gridspec_kw)

    # Create empty object array to hold all axes.  It's easiest to make it 1-d
    # so we can just append subplots upon creation, and then
    nplots = nrows*ncols
    axarr = np.empty(nplots, dtype=object)

    # Create first subplot separately, so we can share it if requested
    ax0 = fig.add_subplot(gs[0, 0], **subplot_kw)
    axarr[0] = ax0

    r, c = np.mgrid[:nrows, :ncols]
    r = r.flatten() * ncols
    c = c.flatten()
    lookup = {
            "none": np.arange(nplots),
            "all": np.zeros(nplots, dtype=int),
            "row": r,
            "col": c,
            }
    sxs = lookup[sharex]
    sys = lookup[sharey]

    # Note off-by-one counting because add_subplot uses the MATLAB 1-based
    # convention.
    for i in range(1, nplots):
        if sxs[i] == i:
            subplot_kw['sharex'] = None
        else:
            subplot_kw['sharex'] = axarr[sxs[i]]
        if sys[i] == i:
            subplot_kw['sharey'] = None
        else:
            subplot_kw['sharey'] = axarr[sys[i]]
        axarr[i] = fig.add_subplot(gs[i // ncols, i % ncols], **subplot_kw)

    # returned axis array will be always 2-d, even if nrows=ncols=1
    axarr = axarr.reshape(nrows, ncols)

    # turn off redundant tick labeling
    if sharex in ["col", "all"] and nrows > 1:
        # turn off all but the bottom row
        for ax in axarr[:-1, :].flat:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.xaxis.offsetText.set_visible(False)

    if sharey in ["row", "all"] and ncols > 1:
        # turn off all but the first column
        for ax in axarr[:, 1:].flat:
            for label in ax.get_yticklabels():
                label.set_visible(False)
            ax.yaxis.offsetText.set_visible(False)

    if squeeze:
        # Reshape the array to have the final desired dimension (nrow,ncol),
        # though discarding unneeded dimensions that equal 1.  If we only have
        # one subplot, just return it instead of a 1-element array.
        if nplots == 1:
            ret = fig, axarr[0, 0]
        else:
            ret = fig, axarr.squeeze()
    else:
        # returned axis array will be always 2-d, even if nrows=ncols=1
        ret = fig, axarr.reshape(nrows, ncols)

    return ret


def subplot2grid(shape, loc, rowspan=1, colspan=1, **kwargs):
    """
    Create a subplot in a grid.  The grid is specified by *shape*, at
    location of *loc*, spanning *rowspan*, *colspan* cells in each
    direction.  The index for loc is 0-based. ::

      subplot2grid(shape, loc, rowspan=1, colspan=1)

    is identical to ::

      gridspec=GridSpec(shape[0], shape[1])
      subplotspec=gridspec.new_subplotspec(loc, rowspan, colspan)
      subplot(subplotspec)
    """

    fig = gcf()
    s1, s2 = shape
    subplotspec = GridSpec(s1, s2).new_subplotspec(loc,
                                                   rowspan=rowspan,
                                                   colspan=colspan)
    a = fig.add_subplot(subplotspec, **kwargs)
    bbox = a.bbox
    byebye = []
    for other in fig.axes:
        if other == a:
            continue
        if bbox.fully_overlaps(other.bbox):
            byebye.append(other)
    for ax in byebye:
        delaxes(ax)

    return a


def twinx(ax=None):
    """
    Make a second axes that shares the *x*-axis.  The new axes will
    overlay *ax* (or the current axes if *ax* is *None*).  The ticks
    for *ax2* will be placed on the right, and the *ax2* instance is
    returned.

    .. seealso::

       :file:`examples/api_examples/two_scales.py`
          For an example
    """
    if ax is None:
        ax=gca()
    ax1 = ax.twinx()
    return ax1


def twiny(ax=None):
    """
    Make a second axes that shares the *y*-axis.  The new axis will
    overlay *ax* (or the current axes if *ax* is *None*).  The ticks
    for *ax2* will be placed on the top, and the *ax2* instance is
    returned.
    """
    if ax is None:
        ax=gca()
    ax1 = ax.twiny()
    return ax1


def subplots_adjust(*args, **kwargs):
    """
    Tune the subplot layout.

    call signature::

      subplots_adjust(left=None, bottom=None, right=None, top=None,
                      wspace=None, hspace=None)

    The parameter meanings (and suggested defaults) are::

      left  = 0.125  # the left side of the subplots of the figure
      right = 0.9    # the right side of the subplots of the figure
      bottom = 0.1   # the bottom of the subplots of the figure
      top = 0.9      # the top of the subplots of the figure
      wspace = 0.2   # the amount of width reserved for blank space between subplots
      hspace = 0.2   # the amount of height reserved for white space between subplots

    The actual defaults are controlled by the rc file
    """
    fig = gcf()
    fig.subplots_adjust(*args, **kwargs)


def tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Automatically adjust subplot parameters to give specified padding.

    Parameters:

    pad : float
        padding between the figure edge and the edges of subplots, as a fraction of the font-size.
    h_pad, w_pad : float
        padding (height/width) between edges of adjacent subplots.
        Defaults to `pad_inches`.
    rect : if rect is given, it is interpreted as a rectangle
        (left, bottom, right, top) in the normalized figure
        coordinate that the whole subplots area (including
        labels) will fit into. Default is (0, 0, 1, 1).
    """

    fig = gcf()
    fig.tight_layout(pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)


@script_log(module_name)
def box(on=None):
    """
    Turn the axes box on or off.  *on* may be a boolean or a string,
    'on' or 'off'.

    If *on* is *None*, toggle state.
    """
    ax = gca()
    on = _string_to_bool(on)
    if on is None:
        on = not ax.get_frame_on()
    ax.set_frame_on(on)


@script_log(module_name)
def title(s, *args, **kwargs):
    """
    Set a title of the current axes.

    Set one of the three available axes titles. The available titles are
    positioned above the axes in the center, flush with the left edge,
    and flush with the right edge.

    .. seealso::
        See :func:`~matplotlib.pyplot.text` for adding text
        to the current axes

    Parameters
    ----------
    label : str
        Text to use for the title

    fontdict : dict
        A dictionary controlling the appearance of the title text,
        the default `fontdict` is:

            {'fontsize': rcParams['axes.titlesize'],
            'fontweight' : rcParams['axes.titleweight'],
            'verticalalignment': 'baseline',
            'horizontalalignment': loc}

    loc : {'center', 'left', 'right'}, str, optional
        Which title to set, defaults to 'center'

    Returns
    -------
    text : :class:`~matplotlib.text.Text`
        The matplotlib text instance representing the title

    Other parameters
    ----------------
    kwargs : text properties
        Other keyword arguments are text properties, see
        :class:`~matplotlib.text.Text` for a list of valid text
        properties.

    """
    return gca().set_title(s, *args, **kwargs)


@script_log(module_name)
def axis(*v, **kwargs):
    """
    Convenience method to get or set axis properties.

    Calling with no arguments::

      >>> axis()

    returns the current axes limits ``[xmin, xmax, ymin, ymax]``.::

      >>> axis(v)

    sets the min and max of the x and y axes, with
    ``v = [xmin, xmax, ymin, ymax]``.::

      >>> axis('off')

    turns off the axis lines and labels.::

      >>> axis('equal')

    changes limits of *x* or *y* axis so that equal increments of *x*
    and *y* have the same length; a circle is circular.::

      >>> axis('scaled')

    achieves the same result by changing the dimensions of the plot box instead
    of the axis data limits.::

      >>> axis('tight')

    changes *x* and *y* axis limits such that all data is shown. If
    all data is already shown, it will move it to the center of the
    figure without modifying (*xmax* - *xmin*) or (*ymax* -
    *ymin*). Note this is slightly different than in MATLAB.::

      >>> axis('image')

    is 'scaled' with the axis limits equal to the data limits.::

      >>> axis('auto')

    and::

      >>> axis('normal')

    are deprecated. They restore default behavior; axis limits are automatically
    scaled to make the data fit comfortably within the plot box.

    if ``len(*v)==0``, you can pass in *xmin*, *xmax*, *ymin*, *ymax*
    as kwargs selectively to alter just those limits without changing
    the others.

      >>> axis('square')

    changes the limit ranges (*xmax*-*xmin*) and (*ymax*-*ymin*) of
    the *x* and *y* axes to be the same, and have the same scaling,
    resulting in a square plot.

    The xmin, xmax, ymin, ymax tuple is returned

    .. seealso::

        :func:`xlim`, :func:`ylim`
           For setting the x- and y-limits individually.
    """
    return gca().axis(*v, **kwargs)


@script_log(module_name)
def xlabel(s, *args, **kwargs):
    """
    Set the *x* axis label of the current axis.

    Default override is::

      override = {
          'fontsize'            : 'small',
          'verticalalignment'   : 'top',
          'horizontalalignment' : 'center'
          }

    .. seealso::

        :func:`~matplotlib.pyplot.text`
            For information on how override and the optional args work
    """
    return gca().set_xlabel(s, *args, **kwargs)


@script_log(module_name)
def ylabel(s, *args, **kwargs):
    """
    Set the *y* axis label of the current axis.

    Defaults override is::

        override = {
           'fontsize'            : 'small',
           'verticalalignment'   : 'center',
           'horizontalalignment' : 'right',
           'rotation'='vertical' : }

    .. seealso::

        :func:`~matplotlib.pyplot.text`
            For information on how override and the optional args
            work.
    """
    return gca().set_ylabel(s, *args, **kwargs)


@script_log(module_name)
def xlim(*args, **kwargs):
    """
    Get or set the *x* limits of the current axes.

    ::

      xmin, xmax = xlim()   # return the current xlim
      xlim( (xmin, xmax) )  # set the xlim to xmin, xmax
      xlim( xmin, xmax )    # set the xlim to xmin, xmax

    If you do not specify args, you can pass the xmin and xmax as
    kwargs, e.g.::

      xlim(xmax=3) # adjust the max leaving min unchanged
      xlim(xmin=1) # adjust the min leaving max unchanged

    Setting limits turns autoscaling off for the x-axis.

    The new axis limits are returned as a length 2 tuple.

    """
    ax = gca()
    if not args and not kwargs:
        return ax.get_xlim()
    ret = ax.set_xlim(*args, **kwargs)
    return ret


@script_log(module_name)
def ylim(*args, **kwargs):
    """
    Get or set the *y*-limits of the current axes.

    ::

      ymin, ymax = ylim()   # return the current ylim
      ylim( (ymin, ymax) )  # set the ylim to ymin, ymax
      ylim( ymin, ymax )    # set the ylim to ymin, ymax

    If you do not specify args, you can pass the *ymin* and *ymax* as
    kwargs, e.g.::

      ylim(ymax=3) # adjust the max leaving min unchanged
      ylim(ymin=1) # adjust the min leaving max unchanged

    Setting limits turns autoscaling off for the y-axis.

    The new axis limits are returned as a length 2 tuple.
    """
    ax = gca()
    if not args and not kwargs:
        return ax.get_ylim()
    ret = ax.set_ylim(*args, **kwargs)
    return ret


@script_log(module_name)
@docstring.dedent_interpd
def xscale(*args, **kwargs):
    """
    Set the scaling of the *x*-axis.

    call signature::

      xscale(scale, **kwargs)

    The available scales are: %(scale)s

    Different keywords may be accepted, depending on the scale:

    %(scale_docs)s
    """
    gca().set_xscale(*args, **kwargs)


@script_log(module_name)
@docstring.dedent_interpd
def yscale(*args, **kwargs):
    """
    Set the scaling of the *y*-axis.

    call signature::

      yscale(scale, **kwargs)

    The available scales are: %(scale)s

    Different keywords may be accepted, depending on the scale:

    %(scale_docs)s
    """
    gca().set_yscale(*args, **kwargs)


@script_log(module_name)
def xticks(*args, **kwargs):
    """
    Get or set the *x*-limits of the current tick locations and labels.

    ::

      # return locs, labels where locs is an array of tick locations and
      # labels is an array of tick labels.
      locs, labels = xticks()

      # set the locations of the xticks
      xticks( arange(6) )

      # set the locations and labels of the xticks
      xticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )

    The keyword args, if any, are :class:`~matplotlib.text.Text`
    properties. For example, to rotate long labels::

      xticks( arange(12), calendar.month_name[1:13], rotation=17 )
    """
    ax = gca()

    if len(args)==0:
        locs = ax.get_xticks()
        labels = ax.get_xticklabels()
    elif len(args)==1:
        locs = ax.set_xticks(args[0])
        labels = ax.get_xticklabels()
    elif len(args)==2:
        locs = ax.set_xticks(args[0])
        labels = ax.set_xticklabels(args[1], **kwargs)
    else: raise TypeError('Illegal number of arguments to xticks')
    if len(kwargs):
        for l in labels:
            l.update(kwargs)

    return locs, silent_list('Text xticklabel', labels)


@script_log(module_name)
def yticks(*args, **kwargs):
    """
    Get or set the *y*-limits of the current tick locations and labels.

    ::

      # return locs, labels where locs is an array of tick locations and
      # labels is an array of tick labels.
      locs, labels = yticks()

      # set the locations of the yticks
      yticks( arange(6) )

      # set the locations and labels of the yticks
      yticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )

    The keyword args, if any, are :class:`~matplotlib.text.Text`
    properties. For example, to rotate long labels::

      yticks( arange(12), calendar.month_name[1:13], rotation=45 )
    """
    ax = gca()

    if len(args)==0:
        locs = ax.get_yticks()
        labels = ax.get_yticklabels()
    elif len(args)==1:
        locs = ax.set_yticks(args[0])
        labels = ax.get_yticklabels()
    elif len(args)==2:
        locs = ax.set_yticks(args[0])
        labels = ax.set_yticklabels(args[1], **kwargs)
    else: raise TypeError('Illegal number of arguments to yticks')
    if len(kwargs):
        for l in labels:
            l.update(kwargs)


    return ( locs,
             silent_list('Text yticklabel', labels)
             )



@script_log(module_name)
def minorticks_on():
    """
    Display minor ticks on the current plot.

    Displaying minor ticks reduces performance; turn them off using
    minorticks_off() if drawing speed is a problem.
    """
    gca().minorticks_on()


@script_log(module_name)
def minorticks_off():
    """
    Remove minor ticks from the current plot.
    """
    gca().minorticks_off()


@script_log(module_name)
def rgrids(*args, **kwargs):
    """
    Get or set the radial gridlines on a polar plot.

    call signatures::

      lines, labels = rgrids()
      lines, labels = rgrids(radii, labels=None, angle=22.5, **kwargs)

    When called with no arguments, :func:`rgrid` simply returns the
    tuple (*lines*, *labels*), where *lines* is an array of radial
    gridlines (:class:`~matplotlib.lines.Line2D` instances) and
    *labels* is an array of tick labels
    (:class:`~matplotlib.text.Text` instances). When called with
    arguments, the labels will appear at the specified radial
    distances and angles.

    *labels*, if not *None*, is a len(*radii*) list of strings of the
    labels to use at each angle.

    If *labels* is None, the rformatter will be used

    Examples::

      # set the locations of the radial gridlines and labels
      lines, labels = rgrids( (0.25, 0.5, 1.0) )

      # set the locations and labels of the radial gridlines and labels
      lines, labels = rgrids( (0.25, 0.5, 1.0), ('Tom', 'Dick', 'Harry' )

    """
    ax = gca()
    if not isinstance(ax, PolarAxes):
        raise RuntimeError('rgrids only defined for polar axes')
    if len(args)==0:
        lines = ax.yaxis.get_gridlines()
        labels = ax.yaxis.get_ticklabels()
    else:
        lines, labels = ax.set_rgrids(*args, **kwargs)

    return ( silent_list('Line2D rgridline', lines),
             silent_list('Text rgridlabel', labels) )


@script_log(module_name)
def thetagrids(*args, **kwargs):
    """
    Get or set the theta locations of the gridlines in a polar plot.

    If no arguments are passed, return a tuple (*lines*, *labels*)
    where *lines* is an array of radial gridlines
    (:class:`~matplotlib.lines.Line2D` instances) and *labels* is an
    array of tick labels (:class:`~matplotlib.text.Text` instances)::

      lines, labels = thetagrids()

    Otherwise the syntax is::

      lines, labels = thetagrids(angles, labels=None, fmt='%d', frac = 1.1)

    set the angles at which to place the theta grids (these gridlines
    are equal along the theta dimension).

    *angles* is in degrees.

    *labels*, if not *None*, is a len(angles) list of strings of the
    labels to use at each angle.

    If *labels* is *None*, the labels will be ``fmt%angle``.

    *frac* is the fraction of the polar axes radius at which to place
    the label (1 is the edge). e.g., 1.05 is outside the axes and 0.95
    is inside the axes.

    Return value is a list of tuples (*lines*, *labels*):

      - *lines* are :class:`~matplotlib.lines.Line2D` instances

      - *labels* are :class:`~matplotlib.text.Text` instances.

    Note that on input, the *labels* argument is a list of strings,
    and on output it is a list of :class:`~matplotlib.text.Text`
    instances.

    Examples::

      # set the locations of the radial gridlines and labels
      lines, labels = thetagrids( range(45,360,90) )

      # set the locations and labels of the radial gridlines and labels
      lines, labels = thetagrids( range(45,360,90), ('NE', 'NW', 'SW','SE') )
    """
    ax = gca()
    if not isinstance(ax, PolarAxes):
        raise RuntimeError('rgrids only defined for polar axes')
    if len(args)==0:
        lines = ax.xaxis.get_ticklines()
        labels = ax.xaxis.get_ticklabels()
    else:
        lines, labels = ax.set_thetagrids(*args, **kwargs)

    return (silent_list('Line2D thetagridline', lines),
            silent_list('Text thetagridlabel', labels)
            )


# This function was copied as is from matplotlib.pyplot
#This function does not do anything.
def plotting():
    pass

def get_plot_commands():
    """
    Get a sorted list of all of the plotting commands.
    """
    # This works by searching for all functions in this module and
    # removing a few hard-coded exclusions, as well as all of the
    # colormap-setting functions, and anything marked as private with
    # a preceding underscore.

    import inspect

    exclude = set(['colormaps', 'colors', 'connect', 'disconnect',
                   'get_plot_commands', 'get_current_fig_manager',
                   'ginput', 'plotting', 'waitforbuttonpress'])
    exclude |= set(colormaps())
    this_module = inspect.getmodule(get_plot_commands)

    commands = set()
    for name, obj in list(six.iteritems(globals())):
        if name.startswith('_') or name in exclude:
            continue
        if inspect.isfunction(obj) and inspect.getmodule(obj) is this_module:
            commands.add(name)

    commands = list(commands)
    commands.sort()
    return commands


def colors():
    """
    This is a do-nothing function to provide you with help on how
    matplotlib handles colors.

    Commands which take color arguments can use several formats to
    specify the colors.  For the basic built-in colors, you can use a
    single letter

      =====   =======
      Alias   Color
      =====   =======
      'b'     blue
      'g'     green
      'r'     red
      'c'     cyan
      'm'     magenta
      'y'     yellow
      'k'     black
      'w'     white
      =====   =======

    For a greater range of colors, you have two options.  You can
    specify the color using an html hex string, as in::

      color = '#eeefff'

    or you can pass an R,G,B tuple, where each of R,G,B are in the
    range [0,1].

    You can also use any legal html name for a color, for example::

      color = 'red'
      color = 'burlywood'
      color = 'chartreuse'

    The example below creates a subplot with a dark
    slate gray background::

       subplot(111, axisbg=(0.1843, 0.3098, 0.3098))

    Here is an example that creates a pale turquoise title::

      title('Is this the best color?', color='#afeeee')

    """
    pass


def colormaps():
    """
    Matplotlib provides a number of colormaps, and others can be added using
    :func:`~matplotlib.cm.register_cmap`.  This function documents the built-in
    colormaps, and will also return a list of all registered colormaps if called.

    You can set the colormap for an image, pcolor, scatter, etc,
    using a keyword argument::

      imshow(X, cmap=cm.hot)

    or using the :func:`set_cmap` function::

      imshow(X)
      pyplot.set_cmap('hot')
      pyplot.set_cmap('jet')

    In interactive mode, :func:`set_cmap` will update the colormap post-hoc,
    allowing you to see which one works best for your data.

    All built-in colormaps can be reversed by appending ``_r``: For instance,
    ``gray_r`` is the reverse of ``gray``.

    There are several common color schemes used in visualization:

    Sequential schemes
      for unipolar data that progresses from low to high
    Diverging schemes
      for bipolar data that emphasizes positive or negative deviations from a
      central value
    Cyclic schemes
      meant for plotting values that wrap around at the
      endpoints, such as phase angle, wind direction, or time of day
    Qualitative schemes
      for nominal data that has no inherent ordering, where color is used
      only to distinguish categories

    The base colormaps are derived from those of the same name provided
    with Matlab:

      =========   =======================================================
      Colormap    Description
      =========   =======================================================
      autumn      sequential linearly-increasing shades of red-orange-yellow
      bone        sequential increasing black-white color map with
                  a tinge of blue, to emulate X-ray film
      cool        linearly-decreasing shades of cyan-magenta
      copper      sequential increasing shades of black-copper
      flag        repetitive red-white-blue-black pattern (not cyclic at
                  endpoints)
      gray        sequential linearly-increasing black-to-white
                  grayscale
      hot         sequential black-red-yellow-white, to emulate blackbody
                  radiation from an object at increasing temperatures
      hsv         cyclic red-yellow-green-cyan-blue-magenta-red, formed
                  by changing the hue component in the HSV color space
      inferno     perceptually uniform shades of black-red-yellow
      jet         a spectral map with dark endpoints, blue-cyan-yellow-red;
                  based on a fluid-jet simulation by NCSA [#]_
      magma       perceptually uniform shades of black-red-white
      pink        sequential increasing pastel black-pink-white, meant
                  for sepia tone colorization of photographs
      plasma      perceptually uniform shades of blue-red-yellow
      prism       repetitive red-yellow-green-blue-purple-...-green pattern
                  (not cyclic at endpoints)
      spring      linearly-increasing shades of magenta-yellow
      summer      sequential linearly-increasing shades of green-yellow
      viridis     perceptually uniform shades of blue-green-yellow
      winter      linearly-increasing shades of blue-green
      =========   =======================================================

    For the above list only, you can also set the colormap using the
    corresponding pylab shortcut interface function, similar to Matlab::

      imshow(X)
      hot()
      jet()

    The next set of palettes are from the `Yorick scientific visualisation
    package <http://dhmunro.github.io/yorick-doc/>`_, an evolution of
    the GIST package, both by David H. Munro:

      ============  =======================================================
      Colormap      Description
      ============  =======================================================
      gist_earth    mapmaker's colors from dark blue deep ocean to green
                    lowlands to brown highlands to white mountains
      gist_heat     sequential increasing black-red-orange-white, to emulate
                    blackbody radiation from an iron bar as it grows hotter
      gist_ncar     pseudo-spectral black-blue-green-yellow-red-purple-white
                    colormap from National Center for Atmospheric
                    Research [#]_
      gist_rainbow  runs through the colors in spectral order from red to
                    violet at full saturation (like *hsv* but not cyclic)
      gist_stern    "Stern special" color table from Interactive Data
                    Language software
      ============  =======================================================

    The following colormaps are based on the `ColorBrewer
    <http://colorbrewer.org>`_ color specifications and designs developed by
    Cynthia Brewer:

    ColorBrewer Diverging (luminance is highest at the midpoint, and
    decreases towards differently-colored endpoints):

      ========  ===================================
      Colormap  Description
      ========  ===================================
      BrBG      brown, white, blue-green
      PiYG      pink, white, yellow-green
      PRGn      purple, white, green
      PuOr      orange, white, purple
      RdBu      red, white, blue
      RdGy      red, white, gray
      RdYlBu    red, yellow, blue
      RdYlGn    red, yellow, green
      Spectral  red, orange, yellow, green, blue
      ========  ===================================

    ColorBrewer Sequential (luminance decreases monotonically):

      ========  ====================================
      Colormap  Description
      ========  ====================================
      Blues     white to dark blue
      BuGn      white, light blue, dark green
      BuPu      white, light blue, dark purple
      GnBu      white, light green, dark blue
      Greens    white to dark green
      Greys     white to black (not linear)
      Oranges   white, orange, dark brown
      OrRd      white, orange, dark red
      PuBu      white, light purple, dark blue
      PuBuGn    white, light purple, dark green
      PuRd      white, light purple, dark red
      Purples   white to dark purple
      RdPu      white, pink, dark purple
      Reds      white to dark red
      YlGn      light yellow, dark green
      YlGnBu    light yellow, light green, dark blue
      YlOrBr    light yellow, orange, dark brown
      YlOrRd    light yellow, orange, dark red
      ========  ====================================

    ColorBrewer Qualitative:

    (For plotting nominal data, :class:`ListedColormap` should be used,
    not :class:`LinearSegmentedColormap`.  Different sets of colors are
    recommended for different numbers of categories.  These continuous
    versions of the qualitative schemes may be removed or converted in the
    future.)

    * Accent
    * Dark2
    * Paired
    * Pastel1
    * Pastel2
    * Set1
    * Set2
    * Set3

    Other miscellaneous schemes:

      ============= =======================================================
      Colormap      Description
      ============= =======================================================
      afmhot        sequential black-orange-yellow-white blackbody
                    spectrum, commonly used in atomic force microscopy
      brg           blue-red-green
      bwr           diverging blue-white-red
      coolwarm      diverging blue-gray-red, meant to avoid issues with 3D
                    shading, color blindness, and ordering of colors [#]_
      CMRmap        "Default colormaps on color images often reproduce to
                    confusing grayscale images. The proposed colormap
                    maintains an aesthetically pleasing color image that
                    automatically reproduces to a monotonic grayscale with
                    discrete, quantifiable saturation levels." [#]_
      cubehelix     Unlike most other color schemes cubehelix was designed
                    by D.A. Green to be monotonically increasing in terms
                    of perceived brightness. Also, when printed on a black
                    and white postscript printer, the scheme results in a
                    greyscale with monotonically increasing brightness.
                    This color scheme is named cubehelix because the r,g,b
                    values produced can be visualised as a squashed helix
                    around the diagonal in the r,g,b color cube.
      gnuplot       gnuplot's traditional pm3d scheme
                    (black-blue-red-yellow)
      gnuplot2      sequential color printable as gray
                    (black-blue-violet-yellow-white)
      ocean         green-blue-white
      rainbow       spectral purple-blue-green-yellow-orange-red colormap
                    with diverging luminance
      seismic       diverging blue-white-red
      nipy_spectral black-purple-blue-green-yellow-red-white spectrum,
                    originally from the Neuroimaging in Python project
      terrain       mapmaker's colors, blue-green-yellow-brown-white,
                    originally from IGOR Pro
      ============= =======================================================

    The following colormaps are redundant and may be removed in future
    versions.  It's recommended to use the names in the descriptions
    instead, which produce identical output:

      =========  =======================================================
      Colormap   Description
      =========  =======================================================
      gist_gray  identical to *gray*
      gist_yarg  identical to *gray_r*
      binary     identical to *gray_r*
      spectral   identical to *nipy_spectral* [#]_
      =========  =======================================================

    .. rubric:: Footnotes

    .. [#] Rainbow colormaps, ``jet`` in particular, are considered a poor
      choice for scientific visualization by many researchers: `Rainbow Color
      Map (Still) Considered Harmful
      <http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=4118486>`_

    .. [#] Resembles "BkBlAqGrYeOrReViWh200" from NCAR Command
      Language. See `Color Table Gallery
      <http://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml>`_

    .. [#] See `Diverging Color Maps for Scientific Visualization
      <http://www.kennethmoreland.com/color-maps/>`_ by Kenneth Moreland.

    .. [#] See `A Color Map for Effective Black-and-White Rendering of
      Color-Scale Images
      <http://www.mathworks.com/matlabcentral/fileexchange/2662-cmrmap-m>`_
      by Carey Rappaport

    .. [#] Changed to distinguish from ColorBrewer's *Spectral* map.
      :func:`spectral` still works, but
      ``set_cmap('nipy_spectral')`` is recommended for clarity.


    """
    return sorted(cm.cmap_d.keys())


def _setup_pyplot_info_docstrings():
    """
    Generates the plotting and docstring.

    These must be done after the entire module is imported, so it is
    called from the end of this module, which is generated by
    boilerplate.py.
    """
    # Generate the plotting docstring
    import re

    def pad(s, l):
        """Pad string *s* to length *l*."""
        if l < len(s):
            return s[:l]
        return s + ' ' * (l - len(s))

    commands = get_plot_commands()

    first_sentence = re.compile("(?:\s*).+?\.(?:\s+|$)", flags=re.DOTALL)

    # Collect the first sentence of the docstring for all of the
    # plotting commands.
    rows = []
    max_name = 0
    max_summary = 0
    for name in commands:
        doc = globals()[name].__doc__
        summary = ''
        if doc is not None:
            match = first_sentence.match(doc)
            if match is not None:
                summary = match.group(0).strip().replace('\n', ' ')
        name = '`%s`' % name
        rows.append([name, summary])
        max_name = max(max_name, len(name))
        max_summary = max(max_summary, len(summary))

    lines = []
    sep = '=' * max_name + ' ' + '=' * max_summary
    lines.append(sep)
    lines.append(' '.join([pad("Function", max_name),
                           pad("Description", max_summary)]))
    lines.append(sep)
    for name, summary in rows:
        lines.append(' '.join([pad(name, max_name),
                               pad(summary, max_summary)]))
    lines.append(sep)

    plotting.__doc__ = '\n'.join(lines)


@script_log(module_name)
def colorbar(mappable=None, cax=None, ax=None, **kw):
    if mappable is None:
        mappable = gci()
        if mappable is None:
            raise RuntimeError('No mappable was found to use for colorbar '
                               'creation. First define a mappable such as '
                               'an image (with imshow) or a contour set ('
                               'with contourf).')
    if ax is None:
        ax = gca()

    ret = gcf().colorbar(mappable, cax = cax, ax=ax, **kw)
    return ret
colorbar.__doc__ = matplotlib.colorbar.colorbar_doc


@script_log(module_name)
def clim(vmin=None, vmax=None):
    """
    Set the color limits of the current image.

    To apply clim to all axes images do::

      clim(0, 0.5)

    If either *vmin* or *vmax* is None, the image min/max respectively
    will be used for color scaling.

    If you want to set the clim of multiple images,
    use, for example::

      for im in gca().get_images():
          im.set_clim(0, 0.05)

    """
    im = gci()
    if im is None:
        raise RuntimeError('You must first define an image, e.g., with imshow')

    im.set_clim(vmin, vmax)


@script_log(module_name)
def set_cmap(cmap):
    """
    Set the default colormap.  Applies to the current image if any.
    See help(colormaps) for more information.

    *cmap* must be a :class:`~matplotlib.colors.Colormap` instance, or
    the name of a registered colormap.

    See :func:`matplotlib.cm.register_cmap` and
    :func:`matplotlib.cm.get_cmap`.
    """
    cmap = cm.get_cmap(cmap)

    rc('image', cmap=cmap.name)
    im = gci()

    if im is not None:
        im.set_cmap(cmap)



@docstring.copy_dedent(_imread)
def imread(*args, **kwargs):
    return _imread(*args, **kwargs)


@docstring.copy_dedent(_imsave)
def imsave(*args, **kwargs):
    return _imsave(*args, **kwargs)



@script_log(module_name)
@activate_category('2d')
def matshow(A, fignum=None, **kw):
    """
    Display an array as a matrix in a new figure window.

    The origin is set at the upper left hand corner and rows (first
    dimension of the array) are displayed horizontally.  The aspect
    ratio of the figure window is that of the array, unless this would
    make an excessively short or narrow figure.

    Tick labels for the xaxis are placed on top.

    With the exception of *fignum*, keyword arguments are passed to
    :func:`~matplotlib.pyplot.imshow`.  You may set the *origin*
    kwarg to "lower" if you want the first row in the array to be
    at the bottom instead of the top.


    *fignum*: [ None | integer | False ]
      By default, :func:`matshow` creates a new figure window with
      automatic numbering.  If *fignum* is given as an integer, the
      created figure will use this figure number.  Because of how
      :func:`matshow` tries to set the figure aspect ratio to be the
      one of the array, if you provide the number of an already
      existing figure, strange things may happen.

      If *fignum* is *False* or 0, a new figure window will **NOT** be created.
    """
    A = np.asanyarray(A)
    if fignum is False or fignum is 0:
        ax = gca()
    else:
        # Extract actual aspect ratio of array and make appropriately sized figure
        fig = figure(fignum, figsize=figaspect(A))
        ax  = fig.add_axes([0.15, 0.09, 0.775, 0.775])

    im = ax.matshow(A, **kw)
    sci(im)

    return im


@script_log(module_name)
def polar(*args, **kwargs):
    """
    Make a polar plot.

    call signature::

      polar(theta, r, **kwargs)

    Multiple *theta*, *r* arguments are supported, with format
    strings, as in :func:`~matplotlib.pyplot.plot`.

    """
    ax = gca(polar=True)
    ret = ax.plot(*args, **kwargs)
    return ret


@script_log(module_name)
def plotfile(fname, cols=(0,), plotfuncs=None,
             comments='#', skiprows=0, checkrows=5, delimiter=',',
             names=None, subplots=True, newfig=True, **kwargs):
    """
    Plot the data in in a file.

    *cols* is a sequence of column identifiers to plot.  An identifier
    is either an int or a string.  If it is an int, it indicates the
    column number.  If it is a string, it indicates the column header.
    matplotlib will make column headers lower case, replace spaces with
    underscores, and remove all illegal characters; so ``'Adj Close*'``
    will have name ``'adj_close'``.

    - If len(*cols*) == 1, only that column will be plotted on the *y* axis.

    - If len(*cols*) > 1, the first element will be an identifier for
      data for the *x* axis and the remaining elements will be the
      column indexes for multiple subplots if *subplots* is *True*
      (the default), or for lines in a single subplot if *subplots*
      is *False*.

    *plotfuncs*, if not *None*, is a dictionary mapping identifier to
    an :class:`~matplotlib.axes.Axes` plotting function as a string.
    Default is 'plot', other choices are 'semilogy', 'fill', 'bar',
    etc.  You must use the same type of identifier in the *cols*
    vector as you use in the *plotfuncs* dictionary, e.g., integer
    column numbers in both or column names in both. If *subplots*
    is *False*, then including any function such as 'semilogy'
    that changes the axis scaling will set the scaling for all
    columns.

    *comments*, *skiprows*, *checkrows*, *delimiter*, and *names*
    are all passed on to :func:`matplotlib.pylab.csv2rec` to
    load the data into a record array.

    If *newfig* is *True*, the plot always will be made in a new figure;
    if *False*, it will be made in the current figure if one exists,
    else in a new figure.

    kwargs are passed on to plotting functions.

    Example usage::

      # plot the 2nd and 4th column against the 1st in two subplots
      plotfile(fname, (0,1,3))

      # plot using column names; specify an alternate plot type for volume
      plotfile(fname, ('date', 'volume', 'adj_close'),
                                    plotfuncs={'volume': 'semilogy'})

    Note: plotfile is intended as a convenience for quickly plotting
    data from flat files; it is not intended as an alternative
    interface to general plotting with pyplot or matplotlib.
    """

    if newfig:
        fig = figure()
    else:
        fig = gcf()

    if len(cols)<1:
        raise ValueError('must have at least one column of data')

    if plotfuncs is None:
        plotfuncs = dict()
    r = mlab.csv2rec(fname, comments=comments, skiprows=skiprows,
                     checkrows=checkrows, delimiter=delimiter, names=names)

    def getname_val(identifier):
        'return the name and column data for identifier'
        if is_string_like(identifier):
            return identifier, r[identifier]
        elif is_numlike(identifier):
            name = r.dtype.names[int(identifier)]
            return name, r[name]
        else:
            raise TypeError('identifier must be a string or integer')

    xname, x = getname_val(cols[0])
    ynamelist = []

    if len(cols)==1:
        ax1 = fig.add_subplot(1,1,1)
        funcname = plotfuncs.get(cols[0], 'plot')
        func = getattr(ax1, funcname)
        func(x, **kwargs)
        ax1.set_ylabel(xname)
    else:
        N = len(cols)
        for i in range(1,N):
            if subplots:
                if i==1:
                    ax = ax1 = fig.add_subplot(N-1,1,i)
                else:
                    ax = fig.add_subplot(N-1,1,i, sharex=ax1)
            elif i==1:
                ax = fig.add_subplot(1,1,1)

            yname, y = getname_val(cols[i])
            ynamelist.append(yname)

            funcname = plotfuncs.get(cols[i], 'plot')
            func = getattr(ax, funcname)

            func(x, y, **kwargs)
            if subplots:
                ax.set_ylabel(yname)
            if ax.is_last_row():
                ax.set_xlabel(xname)
            else:
                ax.set_xlabel('')

    if not subplots:
        ax.legend(ynamelist, loc='best')

    if xname=='date':
        fig.autofmt_xdate()


def _autogen_docstring(base):
    """Autogenerated wrappers will get their docstring from a base function
    with an addendum."""
    msg = "\n\nAdditional kwargs: hold = [True|False] overrides default hold state"
    addendum = docstring.Appender(msg, '\n\n')
    return lambda func: addendum(docstring.copy_dedent(base)(func))

# This function cannot be generated by boilerplate.py because it may
# return an image or a line.
@_autogen_docstring(Axes.spy)
@script_log(module_name)
def spy(Z, precision=0, marker=None, markersize=None, aspect='equal', hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.spy(Z, precision, marker, markersize, aspect, **kwargs)
    finally:
        ax.hold(washold)
    if isinstance(ret, cm.ScalarMappable):
        sci(ret)
    return ret


# The following comment was copied as is matplotlib.pyplot and is not true for this file
################# REMAINING CONTENT GENERATED BY boilerplate.py ##############



@script_log(module_name)
@_autogen_docstring(Axes.acorr)
def acorr(x, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.acorr(x, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret


# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@script_log(module_name)
@_autogen_docstring(Axes.angle_spectrum)
def angle_spectrum(x, Fs=None, Fc=None, window=None, pad_to=None, sides=None,
                   hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.angle_spectrum(x, Fs=Fs, Fc=Fc, window=window, pad_to=pad_to,
                                sides=sides, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost

@script_log(module_name)
@_autogen_docstring(Axes.arrow)
def arrow(x, y, dx, dy, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.arrow(x, y, dx, dy, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@script_log(module_name)
@_autogen_docstring(Axes.axhline)
def axhline(y=0, xmin=0, xmax=1, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.axhline(y=y, xmin=xmin, xmax=xmax, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.axhspan)
@script_log(module_name)
def axhspan(ymin, ymax, xmin=0, xmax=1, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.axhspan(ymin, ymax, xmin=xmin, xmax=xmax, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.axvline)
@script_log(module_name)
def axvline(x=0, ymin=0, ymax=1, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.axvline(x=x, ymin=ymin, ymax=ymax, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.axvspan)
@script_log(module_name)
def axvspan(xmin, xmax, ymin=0, ymax=1, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.axvspan(xmin, xmax, ymin=ymin, ymax=ymax, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.bar)
@script_log(module_name)
def bar(left, height, width=0.8, bottom=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.bar(left, height, width=width, bottom=bottom, data=data,
                     **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.barh)
@script_log(module_name)
def barh(bottom, width, height=0.8, left=None, hold=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.barh(bottom, width, height=height, left=left, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.broken_barh)
@script_log(module_name)
def broken_barh(xranges, yrange, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.broken_barh(xranges, yrange, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@script_log(module_name)
@_autogen_docstring(Axes.boxplot)
def boxplot(x, notch=None, sym=None, vert=None, whis=None, positions=None,
            widths=None, patch_artist=None, bootstrap=None, usermedians=None,
            conf_intervals=None, meanline=None, showmeans=None, showcaps=None,
            showbox=None, showfliers=None, boxprops=None, labels=None,
            flierprops=None, medianprops=None, meanprops=None, capprops=None,
            whiskerprops=None, manage_xticks=True, hold=None, data=None):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.boxplot(x, notch=notch, sym=sym, vert=vert, whis=whis,
                         positions=positions, widths=widths,
                         patch_artist=patch_artist, bootstrap=bootstrap,
                         usermedians=usermedians,
                         conf_intervals=conf_intervals, meanline=meanline,
                         showmeans=showmeans, showcaps=showcaps,
                         showbox=showbox, showfliers=showfliers,
                         boxprops=boxprops, labels=labels,
                         flierprops=flierprops, medianprops=medianprops,
                         meanprops=meanprops, capprops=capprops,
                         whiskerprops=whiskerprops,
                         manage_xticks=manage_xticks, data=data)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.cohere)
@script_log(module_name)
def cohere(x, y, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
           window=mlab.window_hanning, noverlap=0, pad_to=None, sides='default',
           scale_by_freq=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.cohere(x, y, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend,
                        window=window, noverlap=noverlap, pad_to=pad_to,
                        sides=sides, scale_by_freq=scale_by_freq, data=data,
                        **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.clabel)
@script_log(module_name)
def clabel(CS, *args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.clabel(CS, *args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.contour)
@script_log(module_name)
def contour(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.contour(*args, **kwargs)
    finally:
        ax.hold(washold)
    if ret._A is not None: sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.contourf)
@script_log(module_name)
def contourf(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.contourf(*args, **kwargs)
    finally:
        ax.hold(washold)
    if ret._A is not None: sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.csd)
@script_log(module_name)
def csd(x, y, NFFT=None, Fs=None, Fc=None, detrend=None, window=None,
        noverlap=None, pad_to=None, sides=None, scale_by_freq=None,
        return_line=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.csd(x, y, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend,
                     window=window, noverlap=noverlap, pad_to=pad_to,
                     sides=sides, scale_by_freq=scale_by_freq,
                     return_line=return_line, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.errorbar)
@activate_category('1d')
@script_log(module_name)
def errorbar(x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None,
             capsize=None, barsabove=False, lolims=False, uplims=False,
             xlolims=False, xuplims=False, errorevery=1, capthick=None,
             hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt=fmt, ecolor=ecolor,
                          elinewidth=elinewidth, capsize=capsize,
                          barsabove=barsabove, lolims=lolims, uplims=uplims,
                          xlolims=xlolims, xuplims=xuplims,
                          errorevery=errorevery, capthick=capthick, data=data,
                          **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.eventplot)
@script_log(module_name)
def eventplot(positions, orientation='horizontal', lineoffsets=1, linelengths=1,
              linewidths=None, colors=None, linestyles='solid', hold=None,
              data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.eventplot(positions, orientation=orientation,
                           lineoffsets=lineoffsets, linelengths=linelengths,
                           linewidths=linewidths, colors=colors,
                           linestyles=linestyles, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.fill)
@script_log(module_name)
def fill(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.fill(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.fill_between)
@script_log(module_name)
def fill_between(x, y1, y2=0, where=None, interpolate=False, step=None,
                 hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.fill_between(x, y1, y2=y2, where=where,
                              interpolate=interpolate, step=step, data=data,
                              **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.fill_betweenx)
@script_log(module_name)
def fill_betweenx(y, x1, x2=0, where=None, step=None, hold=None, data=None,
                  **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.fill_betweenx(y, x1, x2=x2, where=where, step=step, data=data,
                               **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.hexbin)
@script_log(module_name)
def hexbin(x, y, C=None, gridsize=100, bins=None, xscale='linear',
           yscale='linear', extent=None, cmap=None, norm=None, vmin=None,
           vmax=None, alpha=None, linewidths=None, edgecolors='none',
           reduce_C_function=np.mean, mincnt=None, marginals=False, hold=None,
           data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.hexbin(x, y, C=C, gridsize=gridsize, bins=bins, xscale=xscale,
                        yscale=yscale, extent=extent, cmap=cmap, norm=norm,
                        vmin=vmin, vmax=vmax, alpha=alpha,
                        linewidths=linewidths, edgecolors=edgecolors,
                        reduce_C_function=reduce_C_function, mincnt=mincnt,
                        marginals=marginals, data=data, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.hist)
@script_log(module_name)
def hist(x, bins=10, range=None, normed=False, weights=None, cumulative=False,
         bottom=None, histtype='bar', align='mid', orientation='vertical',
         rwidth=None, log=False, color=None, label=None, stacked=False,
         hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.hist(x, bins=bins, range=range, normed=normed,
                      weights=weights, cumulative=cumulative, bottom=bottom,
                      histtype=histtype, align=align, orientation=orientation,
                      rwidth=rwidth, log=log, color=color, label=label,
                      stacked=stacked, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.hist2d)
@script_log(module_name)
def hist2d(x, y, bins=10, range=None, normed=False, weights=None, cmin=None,
           cmax=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.hist2d(x, y, bins=bins, range=range, normed=normed,
                        weights=weights, cmin=cmin, cmax=cmax, data=data,
                        **kwargs)
    finally:
        ax.hold(washold)
    sci(ret[-1])
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.hlines)
@script_log(module_name)
def hlines(y, xmin, xmax, colors='k', linestyles='solid', label='', hold=None,
           data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.hlines(y, xmin, xmax, colors=colors, linestyles=linestyles,
                        label=label, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.imshow)
@draw_colorbar(gcf,colorbar)
@script_log(module_name)
@activate_category('2d')
def imshow(X, cmap=None, norm=None, aspect=None, interpolation=None, alpha=None,
           vmin=None, vmax=None, origin=None, extent=None, shape=None,
           filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None,
           hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.imshow(X, cmap=cmap, norm=norm, aspect=aspect,
                        interpolation=interpolation, alpha=alpha, vmin=vmin,
                        vmax=vmax, origin=origin, extent=extent, shape=shape,
                        filternorm=filternorm, filterrad=filterrad,
                        imlim=imlim, resample=resample, url=url, data=data,
                        **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.loglog)
@script_log(module_name)
def loglog(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.loglog(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.magnitude_spectrum)
@script_log(module_name)
def magnitude_spectrum(x, Fs=None, Fc=None, window=None, pad_to=None,
                       sides=None, scale=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.magnitude_spectrum(x, Fs=Fs, Fc=Fc, window=window,
                                    pad_to=pad_to, sides=sides, scale=scale,
                                    data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.pcolor)
@script_log(module_name)
@draw_colorbar(gcf, colorbar)
def pcolor(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.pcolor(*args, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.pcolormesh)
@script_log(module_name)
@draw_colorbar(gcf,colorbar)
def pcolormesh(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.pcolormesh(*args, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.phase_spectrum)
@script_log(module_name)
def phase_spectrum(x, Fs=None, Fc=None, window=None, pad_to=None, sides=None,
                   hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.phase_spectrum(x, Fs=Fs, Fc=Fc, window=window, pad_to=pad_to,
                                sides=sides, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.pie)
@script_log(module_name)
def pie(x, explode=None, labels=None, colors=None, autopct=None,
        pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=None,
        radius=None, counterclock=True, wedgeprops=None, textprops=None,
        center=(0, 0), frame=False, hold=None, data=None):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.pie(x, explode=explode, labels=labels, colors=colors,
                     autopct=autopct, pctdistance=pctdistance, shadow=shadow,
                     labeldistance=labeldistance, startangle=startangle,
                     radius=radius, counterclock=counterclock,
                     wedgeprops=wedgeprops, textprops=textprops, center=center,
                     frame=frame, data=data)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.plot)
@script_log(module_name)
@activate_category('1d')
def plot(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.plot(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.plot_date)
@script_log(module_name)
def plot_date(x, y, fmt='o', tz=None, xdate=True, ydate=False, hold=None,
              data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.plot_date(x, y, fmt=fmt, tz=tz, xdate=xdate, ydate=ydate,
                           data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.psd)
@script_log(module_name)
def psd(x, NFFT=None, Fs=None, Fc=None, detrend=None, window=None,
        noverlap=None, pad_to=None, sides=None, scale_by_freq=None,
        return_line=None, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.psd(x, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend,
                     window=window, noverlap=noverlap, pad_to=pad_to,
                     sides=sides, scale_by_freq=scale_by_freq,
                     return_line=return_line, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.quiver)
@script_log(module_name)
def quiver(*args, **kw):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kw.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.quiver(*args, **kw)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.quiverkey)
@script_log(module_name)
def quiverkey(*args, **kw):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kw.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.quiverkey(*args, **kw)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.scatter)
@script_log(module_name)
def scatter(x, y, s=20, c=None, marker='o', cmap=None, norm=None, vmin=None,
            vmax=None, alpha=None, linewidths=None, verts=None, edgecolors=None,
            hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.scatter(x, y, s=s, c=c, marker=marker, cmap=cmap, norm=norm,
                         vmin=vmin, vmax=vmax, alpha=alpha,
                         linewidths=linewidths, verts=verts,
                         edgecolors=edgecolors, data=data, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.semilogx)
@script_log(module_name)
def semilogx(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.semilogx(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.semilogy)
@script_log(module_name)
def semilogy(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.semilogy(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.specgram)
@script_log(module_name)
def specgram(x, NFFT=None, Fs=None, Fc=None, detrend=None, window=None,
             noverlap=None, cmap=None, xextent=None, pad_to=None, sides=None,
             scale_by_freq=None, mode=None, scale=None, vmin=None, vmax=None,
             hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.specgram(x, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend,
                          window=window, noverlap=noverlap, cmap=cmap,
                          xextent=xextent, pad_to=pad_to, sides=sides,
                          scale_by_freq=scale_by_freq, mode=mode, scale=scale,
                          vmin=vmin, vmax=vmax, data=data, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret[-1])
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.stackplot)
@script_log(module_name)
def stackplot(x, *args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.stackplot(x, *args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.stem)
@script_log(module_name)
def stem(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.stem(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.step)
@script_log(module_name)
def step(x, y, *args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.step(x, y, *args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.streamplot)
@script_log(module_name)
def streamplot(x, y, u, v, density=1, linewidth=None, color=None, cmap=None,
               norm=None, arrowsize=1, arrowstyle='-|>', minlength=0.1,
               transform=None, zorder=1, start_points=None, hold=None, data=None):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.streamplot(x, y, u, v, density=density, linewidth=linewidth,
                            color=color, cmap=cmap, norm=norm,
                            arrowsize=arrowsize, arrowstyle=arrowstyle,
                            minlength=minlength, transform=transform,
                            zorder=zorder, start_points=start_points, data=data)
    finally:
        ax.hold(washold)
    sci(ret.lines)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.tricontour)
@script_log(module_name)
@draw_colorbar(gcf,colorbar)
def tricontour(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.tricontour(*args, **kwargs)
    finally:
        ax.hold(washold)
    if ret._A is not None: sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.tricontourf)
@script_log(module_name)
def tricontourf(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.tricontourf(*args, **kwargs)
    finally:
        ax.hold(washold)
    if ret._A is not None: sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.tripcolor)
@script_log(module_name)
def tripcolor(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.tripcolor(*args, **kwargs)
    finally:
        ax.hold(washold)
    sci(ret)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.triplot)
@script_log(module_name)
def triplot(*args, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kwargs.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.triplot(*args, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.violinplot)
@script_log(module_name)
def violinplot(dataset, positions=None, vert=True, widths=0.5, showmeans=False,
               showextrema=True, showmedians=False, points=100, bw_method=None,
               hold=None, data=None):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.violinplot(dataset, positions=positions, vert=vert,
                            widths=widths, showmeans=showmeans,
                            showextrema=showextrema, showmedians=showmedians,
                            points=points, bw_method=bw_method, data=data)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.vlines)
@script_log(module_name)
def vlines(x, ymin, ymax, colors='k', linestyles='solid', label='', hold=None,
           data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.vlines(x, ymin, ymax, colors=colors, linestyles=linestyles,
                        label=label, data=data, **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.xcorr)
@script_log(module_name)
def xcorr(x, y, normed=True, detrend=mlab.detrend_none, usevlines=True,
          maxlags=10, hold=None, data=None, **kwargs):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.xcorr(x, y, normed=normed, detrend=detrend,
                       usevlines=usevlines, maxlags=maxlags, data=data,
                       **kwargs)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@_autogen_docstring(Axes.barbs)
@script_log(module_name)
def barbs(*args, **kw):
    ax = gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()
    hold = kw.pop('hold', None)
    if hold is not None:
        ax.hold(hold)
    try:
        ret = ax.barbs(*args, **kw)
    finally:
        ax.hold(washold)

    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.cla)
@script_log(module_name)
def cla():
    ret = gca().cla()
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.grid)
@script_log(module_name)
def grid(b=None, which='major', axis='both', **kwargs):
    ret = gca().grid(b=b, which=which, axis=axis, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.legend)
@script_log(module_name)
def legend(*args, **kwargs):
    ret = gca().legend(*args, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.table)
@script_log(module_name)
def table(**kwargs):
    ret = gca().table(**kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.text)
@script_log(module_name)
def text(x, y, s, fontdict=None, withdash=False, **kwargs):
    ret = gca().text(x, y, s, fontdict=fontdict, withdash=withdash, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.annotate)
@script_log(module_name)
def annotate(*args, **kwargs):
    ret = gca().annotate(*args, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.ticklabel_format)
@script_log(module_name)
def ticklabel_format(**kwargs):
    ret = gca().ticklabel_format(**kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.locator_params)
@script_log(module_name)
def locator_params(axis='both', tight=None, **kwargs):
    ret = gca().locator_params(axis=axis, tight=tight, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.tick_params)
@script_log(module_name)
def tick_params(axis='both', **kwargs):
    ret = gca().tick_params(axis=axis, **kwargs)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.margins)
@script_log(module_name)
def margins(*args, **kw):
    ret = gca().margins(*args, **kw)
    return ret

# This function was autogenerated by boilerplate.py.  Do not edit as
# changes will be lost
@docstring.copy_dedent(Axes.autoscale)
@script_log(module_name)
def autoscale(enable=True, axis='both', tight=None):
    ret = gca().autoscale(enable=enable, axis=axis, tight=tight)
    return ret

_setup_pyplot_info_docstrings()
