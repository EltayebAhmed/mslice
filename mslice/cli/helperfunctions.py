from mslice.workspace.histogram_workspace import HistogramWorkspace
from mslice.workspace.base import WorkspaceBase as Workspace
from mslice.workspace.workspace import Workspace as MatrixWorkspace
from mslice.models.alg_workspace_ops import get_axis_range, get_available_axes
from mslice.models.axis import Axis
from mslice.models.workspacemanager.workspace_provider import workspace_exists


def _string_to_axis(string):
    axis = string.split(',')
    if len(axis) != 4:
        raise ValueError('axis should be specified in format <name>,<start>,<end>,<step_size>')
    return Axis(axis[0], axis[1], axis[2], axis[3])


def _string_to_integration_axis(string):
    """Allows step to be omitted and set to default value"""
    axis_str = string.split(',')
    if len(axis_str) < 3:
        raise ValueError('axis should be specified in format <name>,<start>,<end>')
    valid_axis = Axis(axis_str[0], axis_str[1], axis_str[2], 0)
    try:
        valid_axis.step = axis_str[3]
    except IndexError:
        valid_axis.step = valid_axis.end - valid_axis.start
    return valid_axis


def _process_axis(axis, fallback_index, input_workspace, string_function=_string_to_axis):
    available_axes = get_available_axes(input_workspace)
    if axis is None:
        axis = available_axes[fallback_index]
    # check to see if axis is just a name e.g 'DeltaE' or a full binning spec e.g. 'DeltaE,0,1,100'
    if ',' in axis:
        axis = string_function(axis)
    elif axis in available_axes:
        range = get_axis_range(input_workspace, axis)
        range = list(map(float, range))
        axis = Axis(units=axis, start=range[0], end=range[1], step=range[2])
    else:
        raise RuntimeError("Axis '%s' not recognised. Workspace has these axes: %s " %
                           (axis, ', '.join(available_axes)))
    return axis


def _check_workspace_name(workspace):
    if isinstance(workspace, Workspace):
        return
    if not isinstance(workspace, str):
        raise TypeError('InputWorkspace must be a workspace or a workspace name')
    if not workspace_exists(workspace):
        raise TypeError('InputWorkspace %s could not be found.' % workspace)


def _check_workspace_type(workspace, correct_type):
    """Check a PSD workspace is MatrixWorkspace, or non-PSD is the specified type"""
    if workspace.is_PSD:
        if isinstance(workspace, MatrixWorkspace):
            raise RuntimeError("Incorrect workspace type - run MakeProjection first.")
        if not isinstance(workspace, correct_type):
            raise RuntimeError("Incorrect workspace type.")
    else:
        if not isinstance(workspace, MatrixWorkspace):
            raise RuntimeError("Incorrect workspace type.")


# Arguments Validation
def is_slice(*args):
    """
    Checks if args[0] is a WorkspaceBase or HistogramWorkspace
    """
    if len(args) > 0:
        if isinstance(args[0], HistogramWorkspace):
            raise ValueError('Warning: To plot a cut use the plot function instead!')
        elif isinstance(args[0], Workspace):
            return True


def is_cut(*args):
    """
    Checks if args[0] is a HistogramWorkspace
    """
    if len(args) > 0:
        if isinstance(args[0], HistogramWorkspace):
            return True
        elif isinstance(args[0], Workspace):
            raise ValueError('Warning: To plot a slice use the pcolormesh function instead!')
