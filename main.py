import sfdc_profile_merge as profile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-in', action='store', dest='input_file_path',
                    help='relative path to the overwriting profile')
parser.add_argument('-to', action='store', dest='original_file_path',
                    help='relative path to the profile being overwritten')
parser.add_argument('-o', action='store', dest='out_file_name',
                    help='profile that should be created')

args = parser.parse_args()

profile.mergetheseprofiles(
    args.input_file_path, args.original_file_path, args.out_file_name)
