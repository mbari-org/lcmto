
from .parse_lcm import to_dataframe
import scipy.io as sio

def lcm_to_mat(out_file: str, in_file: list, channel: str, data_type: str, package: str):
    """
    Converts a list of logfiles into a single concatenated .mat file.
    
    :param out_file: Destination name and path for .mat file
    :param in_file: List of files, e.g. ['lcmlog-09-09-19.00', 'lcmlog-09-09-19.01']
    :param channel: Channel name to listen to
    :param data_type: Corresponding lcm data type for channel name
    :param package: Containing package to find data_type in
    :return:
    """
    
    df = to_dataframe(in_file, {channel: data_type}, package)
    
    print(f'Writing to MAT-file: {out_file}')
    sio.savemat(out_file, {name: col.values for name, col in df[channel].items()})

    return