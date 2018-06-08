#!/usr/bin/env python3
import sfdc_profile_merge as profile
from os.path import isdir, isfile, join
from os import listdir
from shutil import copyfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-in', action='store', dest='input_file_path',
                    help='relative path to the overwriting profile')
parser.add_argument('-to', action='store', dest='original_file_path',
                    help='relative path to the profile being overwritten')
parser.add_argument('-o', action='store', dest='out_file_name',
                    help='profile that should be created')

args = parser.parse_args()

if isdir(args.input_file_path):
    if isdir(args.original_file_path):
        infiles = [f for f in listdir(
            args.input_file_path) if isfile(join(args.input_file_path, f))]
        infiles = list(filter(lambda x: x.endswith('.profile'), infiles))
        outfiles = [f for f in listdir(
            args.original_file_path) if isfile(join(args.original_file_path, f))]
        outfiles = list(filter(lambda x: x.endswith('.profile'), outfiles))
        filestoprocess = []
        for infile in infiles:
            if infile not in outfiles:
                #TODO copy the file into output directory
                copyfile(join(args.input_file_path, infile), join(
                    args.original_file_path, infile))
            else:
                profile.mergetheseprofiles(
                    join(args.input_file_path, infile), join(
                        args.original_file_path, infile), join(args.original_file_path, infile)) # should probably use output file directory if given
        
    else:
        print('your input was a directory, but the original was a file. Please specifiy a directory')
else:
    if args.out_file_name == None:
        args.out_file_name = args.original_file_path

    profile.mergetheseprofiles(args.input_file_path, args.original_file_path, args.out_file_name)
