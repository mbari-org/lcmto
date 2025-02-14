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

from datetime import datetime
def iso_to_microseconds(iso_time_str):
    dt = datetime.fromisoformat(iso_time_str)
    epoch = datetime(1970, 1, 1)
    return int((dt - epoch).total_seconds() * 1e6)

def to_dataframe(in_file: list, channels: dict, package: str = 'gss', start_time: str = None, end_time: str = None):
    """
    function that parses an lcm logfile given channels and their types. you
    must import the lcm type packages prior to call to this function.
    :param in_file: list of combined filenames and paths, i.e. ['lcmlog-09-09-09.00', 'lcmlog-09-09-09.00']
    :param channels: a dictionary of channel  names and their corresponding datatypes, i.e. {'OICONTROL':'sled_control_t'}
    :param package: string name for package to import, must be in current or PYTHONPATH, i.e. 'oi'
    :return: a dict of dataframes for each channel requested
    """

    i, ct = 0, 0
    rows = list()
    # load the logfile for reading

    data = dict()
    colnames = dict()
    dframe = dict()
    start_time_microsecs = 0
    end_time_microsecs = 1e10

    # check for time filtering
    if start_time is not None or end_time is not None:
        if start_time is not None:
            start_time_microsecs = iso_to_microseconds(start_time)
        if end_time is not None:
            end_time_microsecs = iso_to_microseconds(end_time)
        
    sys.stderr.write(f"Filter: START {start_time_microsecs} | END {end_time_microsecs}\r\n")

    for chan, module in channels.items():
        data[chan] = list()
        colnames[chan] = None
        dframe[chan] = None

    

    for log_name in in_file:

        sys.stderr.write("Processing File: %s\r\n" % log_name)
        printed_eventtime = False
        log = lcm.EventLog(log_name, "r")

        for event in log:
            if not printed_eventtime: 
                sys.stderr.write(f"First event in file: {event.timestamp}\r\n")
                printed_eventtime = True

            # Write out a progress into stderr
            ct += 1
            if ct % 10000 == 0:
                percent_done = float(log.tell()) / float(log.size()) * 100.0
                sys.stderr.write('Progress: %10.2f | Records Found: %i\r' % (percent_done, i))
                sys.stderr.flush()

            # time filter
            if event.timestamp < start_time_microsecs:
                continue
            elif event.timestamp > end_time_microsecs:
                sys.stderr.write("Last message encountered: leaving file.\r\n")
                break
            if event.channel in channels.keys():

                    # data
                    data[event.channel].append(event_data(event, package, channels[event.channel]))

                    # head
                    if colnames[event.channel] is None: colnames[event.channel] = event_headers(event, package,
                                                                                                channels[event.channel])

                    i += 1

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
