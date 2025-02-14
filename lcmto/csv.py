##########################
# lcmtocsv.py
#
# author: Eric Martin 2019 MBARI
#
# function to convert lcm log files from a single channel with known lcm type into a csv
#
###########################
from .parse_lcm import to_dataframe


# lcmto.csv('test.csv',['lcmlog-2019-09-27.01'],'OCEANIMAGING_SLEDCONTROLLER','sled_control_t','oi')
def lcm_to_csv(out_file: str, in_file: list, channel: str, data_type: str, package: str, start_time: str = None, end_time: str = None):
    """
    converts a list of logfiles into a single concatenated csv file
    :param out_file: destination name and path for csv file
    :param in_file: list of files, i.e. ['lcmlog-09-09-19.00','lcmlog-09-09-19.01']
    :param channel: channel name to listen to
    :param data_type: corresponding lcm data type for channel name
    :param package: containing package to find data_type in
    :return:
    """

    df = to_dataframe(in_file, {channel: data_type}, package, start_time, end_time)

    print(f'Writing to CSV-file: {out_file}')
    df[channel].to_csv(out_file, index=False)

    return
