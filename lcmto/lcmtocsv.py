##########################
# lcmtocsv.py
#
# author: Eric Martin 2018 MBARI
#
# script to convert lcm log files from a single channel with known lcm type into a csv
#
###########################

import argparse
import importlib
import sys

import lcm

parser = argparse.ArgumentParser(description='process lcm log files by individual channels')
parser.add_argument('channel', type=str, help='lcm channel name to convert')
parser.add_argument('in_file', type=str, help='lcm log filename to convert', nargs=argparse.REMAINDER)
parser.add_argument('--module', type=str, default='pcomms_t', help='known lcm type name')
parser.add_argument('--package', type=str, default='gss', help='package name of lcm type module')

args = parser.parse_args()

# import lcm libs
gss = importlib.import_module(args.package + '.' + args.module)
gss_t = eval('gss.' + args.module)

# load the logfile for reading

header_out = False

for log_name in args.in_file:

    sys.stderr.write("Processing File: %s\r\n" % log_name)
    log = lcm.EventLog(log_name, "r")

    for event in log:
        if event.channel == args.channel:
            # decode the data if its the channel we want
            msg = gss_t.decode(event.data)

            # ignore the methods in this list
            fields = [field for field in dir(msg) if not field.startswith('_')]

            # one time, write out a header
            if header_out is not True:

                # lcm event info
                sys.stdout.write("evt_channel,")
                sys.stdout.write("evt_number,")
                sys.stdout.write("evt_timestamp,")

                for field in fields:
                    value = getattr(msg, field)

                    if callable(value):
                        continue
                    if type(value) is str or type(value) is str:
                        s = str(field).replace(',', '_')
                        sys.stdout.write("%s," % s)
                        continue

                    try:
                        if len(value) is 0:
                            continue

                        for idx, val in enumerate(value):
                            s = str(field).replace(',', '_')
                            s += "_%s" % idx
                            sys.stdout.write("%s," % s)

                    except TypeError as te:
                        try:
                            s = str("%s," % field)
                            sys.stdout.write(s)

                        except TypeError as te:
                            continue
                    except AttributeError as ae:
                        continue

                header_out = True
                sys.stdout.write("\r\n")

            # NOW DATA OUTPUT
            # lcm event info

            sys.stdout.write("%s," % event.channel)
            sys.stdout.write("%i," % event.eventnum)
            sys.stdout.write("%i," % event.timestamp)

            for field in fields:

                value = getattr(msg, field)

                if callable(value):
                    continue

                if type(value) is str or type(value) is str:
                    s = str(value).replace(',', '_')
                    sys.stdout.write("%s," % s)
                    continue

                if type(value) is int:
                    sys.stdout.write("%i," % value)
                    continue

                if type(value) is bool:
                    sys.stdout.write("%i," % value)
                    continue
                try:
                    if len(value) is 0:
                        continue

                    for val in value:
                        sys.stdout.write("%f," % val)

                except TypeError as te:
                    try:
                        sys.stdout.write("%f," % value)

                    except TypeError as te:
                        continue

                except AttributeError as ae:
                    continue

                sys.stdout.write('\n')
                sys.stdout.flush()

        # Write out a progress into stderr
        percent_done = float(log.tell()) / float(log.size()) * 100.0
        sys.stderr.write('Progress: %10.2f\r' % percent_done)
        sys.stderr.flush()
