"""Python-based tool for audio file track splitting"""

import os
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

from ffcuesplitter.user_service import FileSystemOperations


def create_args_parser():
    """Create argument parser"""

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """   
        The purpose of this program is: given an existing FFmpeg installation, to split a source audio file using provided 'YouTube style' timestamps e.g.: 
        
        00:55:45 Pink Elephants on Parade
        01:20:54 Circle of Life
        02:54:01 Colours of the Wind
        """
        ),
    )

    parser.add_argument(
        "timestamps",
        type=str,
        help="File containing timestamps",
    )
    parser.add_argument("audio", type=str, help="Audio file source")
    parser.add_argument("--artist", dest="artist", type=str, help="Artist name")
    parser.add_argument("--album", dest="album", type=str, help="Album name")
    parser.add_argument(
        "--only-cue",
        action="store_true",
        default=False,
        help="Optional: Output cue file without performing split, when supplied with 'True' argument (Default: False)",
    )

    return parser.parse_args()


def datetime_transform(timecode):
    """
    Detect whether a timecode is %M:%S or %H:%M:%S'
    """

    def hms2msf(timecode_dt):
        """
        Given a datetime object with the %H:%M:%S format, convert to cuesheet compatible %M:%S:%f timestamp, return respective string
        Note: this iteration populates the %f component with a single double-zero padding (:00)
        """
        minutes = timecode_dt.hour * 60 + timecode_dt.minute
        seconds = timecode_dt.second
        msf = f"{minutes}:{seconds:02d}:00"
        return msf

    assert ":" in timecode, "Timecode could not be converted"

    if timecode.count(":") == 1:
        timecode_dt = datetime.strptime(timecode, "%M:%S").time()
        timecode_string = timecode_dt.strftime("%M:%S:00")

    if timecode.count(":") == 2:
        timecode_dt = datetime.strptime(timecode, "%H:%M:%S").time()
        timecode_string = hms2msf(timecode_dt)

    return timecode_string


def extract_timestamps(timestamps_file):
    """
    Given a text file containing 'YouTube-style timestamps' (where timecodes and titles are separated by a single white-space), separate timecodes and track strings into their constituent lists.
    This iteration also converts the time strings into the cue-sheet compatible %M:%S:%f timestamp format.
    """
    timecode_cue = []
    track_string = []

    with open(timestamps_file, "rt", encoding="utf-8") as timestamps:
        for line in timestamps:
            timecode = line.split(" ")[0]
            timecode_string = datetime_transform(timecode)
            timecode_cue.append(timecode_string)
            track_string.append(" ".join(line.split(" ")[1:]))

    return timecode_cue, track_string


def make_cue(timecode, track_string, audio_file, artist, album, out_dir):
    """
    Generates a cue sheet for track splitting, given:
    * timecode and title strings (of eaqual length)
    * source audio filename
    * respective artist (PERFORMER) and album (TITLE)
    """
    # Determine audio codec
    ext_to_codec = {
        "flac": "flac",
        "mp3": "mp3",
        "ogg": "ogg",
        "opus": "opus",
        "ape": "ape",
        "wav": "wave",
        "m4a": "aac",
    }
    audio_codec = ext_to_codec.get(audio_file.split(".")[-1], None)
    assert audio_codec, "Audio codec couldn't be determined"

    # Build cue sheet from timecodes and tracks
    cue_sheet = f'PERFORMER "{artist}"\nTITLE "{album}"\nFILE "{audio_file}" {audio_codec.upper()}\n'

    for i, (track_string, timecode) in enumerate(zip(track_string, timecode)):
        track_number = i + 1
        cue_sheet += f"\tTRACK {track_number:02d} AUDIO\n"
        cue_sheet += f'\t\tTITLE "{track_string}"\n'
        cue_sheet += f"\t\tINDEX 01 {timecode}\n"

    # Write cue sheet
    audiofile_basename = os.path.basename(audio_file)
    cuesheet_filename = os.path.join(
        out_dir, f"{os.path.splitext(audiofile_basename)[0]}.cue"
    )

    with open(cuesheet_filename, "wt", encoding="utf-8") as f:
        f.write(cue_sheet)

    return cuesheet_filename


def get_output_fmt(audio_file):
    """Determine ffcuesplitter output format"""
    valid_formats = ("flac", "mp3", "ogg", "opus")
    file_ext = audio_file.split(".")[-1]
    for fmt in valid_formats:
        if fmt in valid_formats:
            output_fmt = fmt
            return output_fmt
    if file_ext == "wav":
        output_fmt = "wave"
    else:
        output_fmt = "copy"
    return output_fmt


def call_ffcuesplitter(audio_file, cuesheet_filename, out_dir):
    """
    Split source audio file into individual tracks, given a timestamps file using FFmpeg (option to generate cue sheet without performing split)
    """
    output_format = get_output_fmt(audio_file)
    split = FileSystemOperations(
        filename=cuesheet_filename,
        outputdir=out_dir,
        outputformat=f"{output_format}",
        ffmpeg_add_params="-map 0:a",  # to avoid errors with cover art
        dry=False,
        prg_loglevel="info",
    )
    if split.kwargs["dry"]:
        split.dry_run_mode()
    else:
        overwr = split.check_for_overwriting()
        if not overwr:
            split.work_on_temporary_directory()


def main():
    """Main function"""
    args = create_args_parser()

    timestamps_file = args.timestamps
    audio_file = args.audio
    artist = args.artist
    album = args.album
    only_cue = args.only_cue

    out_dir = os.path.join(os.getcwd(), f"{artist}_{album}_tracksplit")
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    timecode, track_string = extract_timestamps(timestamps_file)

    cuesheet_filename = make_cue(
        timecode, track_string, audio_file, artist, album, out_dir
    )

    if not only_cue:
        call_ffcuesplitter(audio_file, cuesheet_filename, out_dir)


if __name__ == "__main__":
    main()
