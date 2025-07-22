##########################
# todataframe.py
#
# author: Eric Martin 2019 MBARI
#
# script to convert lcm log files from a single channel
# with a  known type into memory.  
# 
#
###########################

import argparse
import sys

import lcm
import pandas as pd

from .process import event_data, event_headers


def to_dataframe(in_file: list, channels: dict, package: str = 'gss'):
    """
    function that parses an lcm logfile given channels and their types. you
    must import the lcm type packages prior to call to this function.
    :param in_file: list of combined filenames and paths, i.e. ['lcmlog-09-09-09.00', 'lcmlog-09-09-09.00']
    :param channels: a dictionary of channel  names and their corresponding datatypes, i.e. {'OICONTROL':'sled_control_t'}
    :param package: string name for package to import, must be in current or PYTHONPATH, i.e. 'oi'
    :return: a dict of dataframes for each channel requested
    """

    i = 0
    rows = list()
    # load the logfile for reading

    data = dict()
    colnames = dict()
    dframe = dict()

    for chan, module in channels.items():
        data[chan] = list()
        colnames[chan] = None
        dframe[chan] = None

    # print(data)
    for log_name in in_file:

        sys.stderr.write("Processing File: %s\r\n" % log_name)
        log = lcm.EventLog(log_name, "r")

        for event in log:
            if event.channel in channels.keys():

                # data
                data[event.channel].append(event_data(event, package, channels[event.channel]))

                # head
                if colnames[event.channel] is None: colnames[event.channel] = event_headers(event, package,
                                                                                            channels[event.channel])

                i += 1

                # Write out a progress into stderr
                percent_done = float(log.tell()) / float(log.size()) * 100.0
                sys.stderr.write('Progress: %10.2f | Records Found: %i\r' % (percent_done, i))
                sys.stderr.flush()

    sys.stderr.write('\n')

    for chan in channels:
        dframe[chan] = pd.DataFrame(data[chan], columns=colnames[chan])
    return dframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process lcm log files by individual channels')
    parser.add_argument('out_file', type=str, help='filename for output pickle file')
    parser.add_argument('in_file', type=str, help='lcm log filename to convert', nargs=argparse.REMAINDER)
    parser.add_argument('--package', type=str, default='gss', help='package name of lcm type module')
    args = parser.parse_args()

    # Parse for
    channels = {
        'SOI_NAV_SOLUTION': 'nav_solution_t',
        'SEABIRD_CTD_STAT': 'pcomms_t',
    }

    df = to_dataframe(args.in_file, channels, args.package)
