import logging
import os
try:
    from ConfigParser import ConfigParser as _ConfigParser
except ImportError:
    from configparser import ConfigParser as _ConfigParser
from datetime import datetime, timedelta, tzinfo
from tabpy.tabpy_server.app.ConfigParameters import ConfigParameters
from tabpy.tabpy_server.app.SettingsParameters import SettingsParameters


def write_state_config(state, settings, logger=logging.getLogger(__name__)):
    if SettingsParameters.StateFilePath in settings:
        state_path = settings[SettingsParameters.StateFilePath]
    else:
        msg = f'{ConfigParameters.TABPY_STATE_PATH} is not set'
        logger.log(logging.CRITICAL, msg)
        raise ValueError(msg)

    logger.log(logging.DEBUG, f'State path is {state_path}')
    state_key = os.path.join(state_path, 'state.ini')
    tmp_state_file = state_key

    with open(tmp_state_file, 'w') as f:
        state.write(f)


def _get_state_from_file(state_path, logger=logging.getLogger(__name__)):
    state_key = os.path.join(state_path, 'state.ini')
    tmp_state_file = state_key

    if not os.path.exists(tmp_state_file):
        msg = f'Missing config file at {tmp_state_file}'
        logger.log(logging.CRITICAL, msg)
        raise ValueError(msg)

    config = _ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(tmp_state_file)

    if not config.has_section('Service Info'):
        msg = ('Config error: Expected [Service Info] section in '
               f'{tmp_state_file}')
        logger.log(logging.CRITICAL, msg)
        raise ValueError(msg)

    return config


_ZERO = timedelta(0)


class _UTC(tzinfo):
    """
    A UTC datetime.tzinfo class modeled after the pytz library. It includes a
    __reduce__ method for pickling,
    """

    def fromutc(self, dt):
        if dt.tzinfo is None:
            return self.localize(dt)
        return super(_UTC, self).fromutc(dt)

    def utcoffset(self, dt):
        return _ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _ZERO

    def __reduce__(self):
        return _UTC, ()

    def __repr__(self):
        return "<UTC>"

    def __str__(self):
        return "UTC"
