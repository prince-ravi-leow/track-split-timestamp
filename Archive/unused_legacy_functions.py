#!/usr/bin/env python3

import csv
import re
from datetime import datetime

def extract_elements_csv(timestamps_file):    
	"""
	(CURRENTLY UNUSED)
	Same as extract_elements() (see respective docstring), uses csv module and doesn't perform %M:%S:%f conversion.
	
	Function has been preserved:
	* as a fall-back, should the current method (string split) become less reliable
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

def extract_elements_regex(timestamps_file):
	"""
	(CURRENTLY UNUSED)
	Same as extract_elements() (see respective docstring)
    (Won't work without hms2msf() func, in main tracksplit.py script) 
    Uses re module to parse the string, before and after the first white-space such that:
	* Before: timestamp
	* After: trackname
	
	Function has been preserved:
	* as a fall-back, should the current method (string split) become less reliable
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