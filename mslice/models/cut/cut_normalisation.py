import numpy as np
from mantid.api import IMDHistoWorkspace, MDNormalization

def _normalize_workspace(workspace):
    assert isinstance(workspace, IMDHistoWorkspace)
    num_events = workspace.getNumEventsArray()
    average_event_intensity = _num_events_normalized_array(workspace)
    average_event_range = average_event_intensity.max() - average_event_intensity.min()

    normed_average_event_intensity = (average_event_intensity - average_event_intensity.min())/average_event_range
    if workspace.displayNormalization() == MDNormalization.NoNormalization:
        new_data = normed_average_event_intensity
    else:
        new_data = normed_average_event_intensity * num_events
    new_data = np.array(new_data)

    new_data = np.nan_to_num(new_data)
    workspace.setSignalArray(new_data)

    errors = workspace.getErrorSquaredArray() / (average_event_range**2)
    workspace.setErrorSquaredArray(errors)
    workspace.setComment("Normalized By MSlice")

def _num_events_normalized_array(workspace):
    assert isinstance(workspace, IMDHistoWorkspace)
    with np.errstate(invalid='ignore'):
        if workspace.displayNormalization() == MDNormalization.NoNormalization:
            data = np.array(workspace.getSignalArray())
            data[np.where(workspace.getNumEventsArray() == 0)] = np.nan
        else:
            data = workspace.getSignalArray() / workspace.getNumEventsArray()
    data = np.ma.masked_where(np.isnan(data), data)
    return data
