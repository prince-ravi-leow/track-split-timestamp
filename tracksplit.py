#!/usr/bin/env python3

# Wishlist:
# * Option to process video files 

import os
import re
import csv
from datetime import datetime

def hms2msf(timecode_dt):
	"""
	Given a datetime object with the %H:%M:%S format, convert to cue-sheet compatible %M:%S:%f timestamp and return respective string (note that this iteration populates the %f component with a single double-zero padding (:00))
	"""
	minutes = timecode_dt.hour*60 + timecode_dt.minute
	seconds = timecode_dt.second
	msf = f"{minutes}:{seconds:02d}:00"
	return msf


def extract_elements(timestamps_file):
	"""
	Given a text file containing 'YouTube-style timestamps' (where timecodes and titles are separated by a single white-space) separate timecodes and track strings into their constituent lists. This iteration also converts the time strings into the cue-sheet compatible %M:%S:%f timestamp format.
	"""
	pattern = r'^([^ ]+)\s(.+)$'
	timecode_cue = []
	track_string = []
	with open(timestamps_file, "rt") as timestamps:
		for line in timestamps:
			match = re.search(pattern, line)
			if match:
				track_string.append(match.group(2).rstrip())
				timecode = match.group(1)
				if timecode.count(":") == 1:
					timecode_dt = datetime.strptime(timecode, '%M:%S').time()
					timecode_cue.append(timecode_dt.strftime('%M:%S:%f'))
				if timecode.count(":") == 2:
					timecode_dt = datetime.strptime(timecode, '%H:%M:%S').time()
					timecode_cue.append(hms2msf(timecode_dt))
	return timecode_cue, track_string 

def df2cue(timecode, track_string, audio_file, artist, album):
	"""
	Generates a cue sheet for track splitting, given: 
	* timecode and title strings (of eaqual length)
	* source audio filename
	* respective artist (PERFORMER) and album (TITLE)
	"""
	file_ext = audio_file.split(".")[-1]
	if file_ext == 'wav':
		file_type = 'wave'
	else:
		file_type = file_ext
	cue_sheet = f'PERFORMER "{artist}"\nTITLE "{album}"\nFILE "{audio_file}" {file_type.upper()}\n'
	for i in range(len(timecode)):
		track_number = i + 1
		cue_sheet += f'\tTRACK {track_number:02d} AUDIO\n'
		cue_sheet += f'\t\tTITLE "{track_string[i]}"\n'
		cue_sheet += f'\t\tINDEX 01 {timecode[i]}\n'
	return cue_sheet

def extract_elements_csv(timestamps_file):    
	"""
	(CURRENTLY UNUSED)
	Same as extract_elements() (see respective docstring), uses csv module and doesn't perform %M:%S:%f conversion.
	
	Function has been preserved:
	* as a fall-back, should the regex option become less reliable
	* as a basis for possible full support for timestamps in delimited (tsv, csv, etc.) file formats, further down the road
	"""
	timecodes = []
	track_strings = []
	with open(timestamps_file, "rt") as handle:
		timestamps = csv.reader(handle, delimiter=' ')
		for i,row in enumerate(timestamps):
			timecodes.append(row[0])
			conc_strings = []
			for strings in row[1:]:
				conc_strings += strings+" "
			track_strings.append(''.join(conc_strings).rstrip())
	return timecodes, track_strings

def main():
	"""
	Split source audio file into individual tracks, given a timestamps file using FFmpeg (option to generate cue sheet without performing split)
	"""
	timecode, track_string = extract_elements(timestamps_file)

	cue_sheet = df2cue(timecode, track_string, audio_file, artist, album)
	with open('cue_sheet.cue', "wt") as f:
		f.write(cue_sheet)
	if not only_cue:
		try:
			from ffcuesplitter.user_service import FileSystemOperations
		except ImportError:
			print("The required module 'ffcuesplitter' is not found.")
			print("Please install it by running 'python3 -m pip install ffcuesplitter'")
			exit(1)
		if not os.path.exists("cue_project_output/"):
			os.mkdir("cue_project_output/")
		else:
			file_type = audio_file.split(".")[-1]    
			split = FileSystemOperations(
				filename='cue_sheet.cue',
				outputdir='cue_project_output', 
				outputformat=f"{file_type}",
				ffmpeg_add_params='-map 0:a', # to avoid errors with cover art 
				dry=False, 
				prg_loglevel='info')
			if split.kwargs['dry']:
				split.dry_run_mode()
			else:
				overwr = split.check_for_overwriting()
				if not overwr:
					split.work_on_temporary_directory()
	return

if __name__ == '__main__':
	from argparse import ArgumentParser
	from argparse import RawDescriptionHelpFormatter
	import textwrap

	parser = ArgumentParser(
		formatter_class = RawDescriptionHelpFormatter,
		description = textwrap.dedent("""
		
		*** EXAMPLE USAGE: *** 

		./tracksplit.py --timestamps 'timestamps.txt' --audio 'concert_audio.mp3' --artist 'Sensible Clown Conglomerate' --album 'The Light Side of the Sun'
		
		The purpose of this program is: given an existing FFmpeg installation, to split a source audio file using provided 'YouTube style' timestamps e.g.: 
		
		00:55:45 Pink Elephants on Parade
		01:20:54 Circle of Life
		02:54:01 Colours of the Wind

		Running the entire track-splitting pipeline requires a single Python dependency (FFcuesplitter).

		*HOWEVER*, should one desire to perform the actual track split with a software of their choice, one can obtain a source audio file-specific cue sheet by providing setting the --only-cue to True, which will BYPASS the dependency entirely.
		"""))

	parser.add_argument("--timestamps", action="store", dest="timestamps_file", type=str, help="File containing timestamps")
	parser.add_argument("--audio", action="store", dest="audio_file", type=str, help="Source audio file")
	parser.add_argument("--artist", action="store", dest="artist", type=str, help="Artist name")
	parser.add_argument("--album", action="store", dest="album", type=str, help="Album name")
	parser.add_argument("--only-cue", action="store", dest="only_cue", type=bool, default=False, help="Optional: Output cue file without performing split, when supplied with 'True' argument (Default: False)")

	args = parser.parse_args()
	timestamps_file = args.timestamps_file
	audio_file = args.audio_file
	artist = args.artist
	album = args.album
	only_cue = args.only_cue

	main()