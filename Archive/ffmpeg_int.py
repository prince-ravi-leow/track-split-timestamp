#!/usr/bin/env python3

import os
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser(description="Interface Python with ffmpeg")

parser.add_argument("-i", action="store", dest="input", help="Input file")
parser.add_argument("-o", action="store", dest="output", help="Output file")
parser.add_argument("--add_args", nargs="+", dest="add_args", help="Output file name")

args = parser.parse_args()
input = args.input
output = args.output
add_args = args.add_args

#ffmpeg -i input.mp4 output.avi

cmd = f"ffmpeg -i {input}"

if add_args:
    cmd += " " + " ".join(add_args)

if output:
    cmd += f" {output}"

subprocess.run(cmd, shell=True, check=True)