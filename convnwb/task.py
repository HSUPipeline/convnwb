"""Base task class."""

from copy import deepcopy

import numpy as np

from convnwb.timestamps import predict_times
from convnwb.utils import is_empty, offset_time, change_time_units

###################################################################################################
###################################################################################################

TIME_UPDATES = {
    'offset' : offset_time,
    'change_units' : change_time_units,
    'predict_times' : predict_times,
}

class TaskBase():
    """Base object for collecting task information."""

    def __init__(self):
        """Initialize TaskBase object."""

        # Define information about the status of the task object
        self.status = {
            'time_aligned' : False,
            'time_reset' : False,
            'time_offset' : None,
        }

        # Metadata - subject / session information
        self.meta = {
            'task' : None,
            'subject' : None,
            'session' : None
        }

        # Experiment information
        self.experiment = {
            'version' : {'label' : None, 'number' : None},
            'language' : None,
        }

        # Environment information
        self.environment = {}

        # Session information
        self.session = {
            'start_time' : None,
            'end_time' : None
        }

        # Synchronization information
        self.sync = {
            # Synchronization pulses
            'neural' : {},
            'behavioral' : {},
            # Synchronization alignment
            'alignment' : {
                'intercept' : None,
                'coef' : None,
                'score' : None
            }
        }

        # Position related information
        self.position = {
            'time' : [],
            'x' : [],
            'y' : [],
            'z' : [],
            'speed' : []
        }

        # Head direction information
        self.head_direction = {
            'time' : [],
            'degrees' : [],
        }

        # Information about timing of task phases
        self.phase_times = {}

        # Stimulus information
        self.stimuli = {}

        # Trial information
        self.trial = {}

        # Response information
        self.responses = {}


    def copy(self):
        """Return a deepcopy of this object."""

        return deepcopy(self)


    def data_keys(self, skip=None):
        """Get a list of data keys defined in the task object.

        Parameters
        ----------
        skip : str or list of str
            Name(s) of any data attributes to skip.

        Returns
        -------
        data_keys : list of str
            List of data attributes available in the object.
        """

        data_keys = list(vars(self).keys())

        # Drop the 'status' attribute, which doesn't store data
        data_keys.remove('status')

        if skip:
            for skip_item in [skip] if isinstance(skip, str) else skip:
                data_keys.remove(skip_item)

        return data_keys


    def convert_to_array(self, field, keys, dtype):
        """Convert data fields to numpy arrays.

        Parameters
        ----------
        field : str
            Which field to access data to convert from.
        keys : list of str
            Which key(s) of the field to convert to array.
        dtype : type
            The data type to give the converted array.
        """

        data = getattr(self, field)
        for key in [keys] if isinstance(keys, (str, dict)) else keys:
            if isinstance(key, str):
                data[key] = np.array(data[key]).astype(dtype)
            else:
                for okey, ikeys in key.items():
                    for ikey in [ikeys] if isinstance(ikeys, str) else ikeys:
                        data[okey][ikey] = np.array(data[okey][ikey]).astype(dtype)


    def get_trial(self, index, field=None):
        """Get the information for a specified trial.

        Parameters
        ----------
        index : int
            The index of the trial to access.
        field : str, optional, default: None
            Which trial data to access.
        """

        trial_data = getattr(self, 'trial')
        if field:
            trial_data = trial_data[field]

        trial_info = dict()
        for key in trial_data.keys():
            # Collect trial info, skipping dictionaries, which are subevents
            if not isinstance(trial_data[key], dict):
                trial_info[key] = trial_data[key][index]

        return trial_info


    def plot_sync_allignment(self, n_pulses=100):
        """Plots alignment of the synchronization pulses.

        Parameters
        ----------
        n_pulses : int, optional, default: 100
            Number of pulses to plot for zoomed plot.
        """

        # should be implemented in subclass
        raise NotImplementedError


    def update_time(self, update, skip=None, **kwargs):
        """Offset all timestamps within the task object.

        Parameters
        ----------
        update : {'offset', 'change_units'} or callable
            What kind of update to do to the timestamps.
        kwargs
            Additional arguments to pass to the update function.
        skip : str or list of str, optional
            Any data fields to
        """

        # Select update function to use
        if isinstance(update, str):
            assert update in ['offset', 'change_units'], \
                "Update approach doesn't match whats available: offset', 'change_units"
            func = TIME_UPDATES[update]
        else:
            func = update

        # Update any fields with 'time' in their name
        #   Note: this update goes down up to two levels of embedded dictionaries
        for field in self.data_keys(skip):
            data = getattr(self, field)
            for key in data.keys():
                if isinstance(data[key], dict):
                    for subkey in data[key].keys():
                        if 'time' in subkey and not is_empty(data[key][subkey]):
                            data[key][subkey] = func(data[key][subkey], **kwargs)
                else:
                    if 'time' in key and not is_empty(data[key]):
                        data[key] = func(data[key], **kwargs)

        # Update status information about the reset
        if update == 'offset':
            self.status['time_reset'] = True
            self.status['time_offset'] = kwargs['offset']