#!/usr/bin/env python3

# Wishlist:
# * Option to process video files 

import os
from datetime import datetime

def hms2msf(timecode_dt):
	"""
	Given a datetime object with the %H:%M:%S format, 
	convert to cuesheet compatible %M:%S:%f timestamp,
	return respective string 
	Note: this iteration populates the %f component with a single double-zero padding (:00)
	"""
	minutes = timecode_dt.hour*60 + timecode_dt.minute
	seconds = timecode_dt.second
	msf = f"{minutes}:{seconds:02d}:00"
	return msf

def datetime_transform(timecode):
	"""
	Detect whether a timecode is %M:%S or %H:%M:%S' 
	(uses the revolutionary method of COUNTING number of colons 
	- AMAZING I know!), 
	uses datetime module and hms2msf helping function to return a cuesheet compatible timecode string
	"""
	if timecode.count(":") == 1:
		timecode_dt = datetime.strptime(timecode, '%M:%S').time()
		timecode_string = timecode_dt.strftime('%M:%S:00')
	if timecode.count(":") == 2:
		timecode_dt = datetime.strptime(timecode, '%H:%M:%S').time()
		timecode_string = hms2msf(timecode_dt)
	return timecode_string

def extract_elements(timestamps_file):
	"""
	Given a text file containing 'YouTube-style timestamps' (where timecodes and titles are separated by a single white-space), 
	separate timecodes and track strings into their constituent lists. 
	This iteration also converts the time strings into the cue-sheet compatible %M:%S:%f timestamp format.
	"""
	timecode_cue = []
	track_string = []
	with open(timestamps_file, "rt") as timestamps:
		for line in timestamps:
			timecode = line.split(" ")[0]
			timecode_string = datetime_transform(timecode)
			timecode_cue.append(timecode_string)
			track_string.append(" ".join(line.split(" ")[1:]))	
	return timecode_cue, track_string 

def make_cue(timecode, track_string, audio_file, artist, album):
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
	audiofile_basename = os.path.basename(audio_file)	
	cuesheet_filename = f"{os.path.splitext(audiofile_basename)[0]}.cue"
	with open(cuesheet_filename, "wt") as f:
		f.write(cue_sheet)
	return cuesheet_filename

def tracksplit():
	"""
	Split source audio file into individual tracks, given a timestamps file using FFmpeg (option to generate cue sheet without performing split)
	"""
	timecode, track_string = extract_elements(timestamps_file)

	cuesheet_filename = make_cue(timecode, track_string, audio_file, artist, album)
		
	if not only_cue:
		out_dir = os.path.join(os.getcwd(), f'{artist}_{album}_tracksplit')
		if not os.path.exists(out_dir):
			os.mkdir(out_dir)
		else:
			try:
				from ffcuesplitter.user_service import FileSystemOperations
			except ImportError:
				print("The required module 'ffcuesplitter' is not found.")
				print("Please install it by running 'python3 -m pip install ffcuesplitter'")
				exit(1)
			file_type = audio_file.split(".")[-1]    
			split = FileSystemOperations(
				filename = cuesheet_filename,
				outputdir = out_dir, 
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

		HOWEVER, should one desire to perform the actual track split with a software of their choice, one can obtain a source audio file-specific cue sheet by providing setting the --only-cue to True, which will BYPASS the dependency entirely.
		"""))

	parser.add_argument(
		"--timestamps", 
		action="store", 
		dest="timestamps_file", 
		type=str, 
		help="File containing timestamps")
	parser.add_argument(
		"--audio", 
		action="store", 
		dest="audio_file", 
		type=str, 
		help="Source audio file")
	parser.add_argument(
		"--artist", 
		action="store", 
		dest="artist", 
		type=str, 
		help="Artist name")
	parser.add_argument(
		"--album", 
		action="store", 
		dest="album", 
		type=str, 
		help="Album name")
	parser.add_argument(
		"--only-cue", 
		action="store", 
		dest="only_cue", 
		type=bool, 
		default=False, 
		help="Optional: Output cue file without performing split, when supplied with 'True' argument (Default: False)")

	args = parser.parse_args()
	timestamps_file = args.timestamps_file
	audio_file = args.audio_file
	artist = args.artist
	album = args.album
	only_cue = args.only_cue

	tracksplit()