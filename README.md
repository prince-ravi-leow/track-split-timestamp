# Python-based tool for audio file track splitting
The purpose of this program is to provide a convenient way to perform audio file track-splitting, using simple 'YouTube style' timestamps. 

E.g.
```
00:55:45 Pink Elephants on Parade
01:20:54 Circle of Life
02:54:01 Colours of the Wind
```

I created this script, because of my personal hobby of taking concert audio, and splitting it into tracks, so that I could re-package and enjoy it as an 'album'. 

## Pipeline
In short, this script:
1) Generates takes the audio/timestamps files, and generates a [cue sheet](https://en.wikipedia.org/wiki/Cue_sheet_(computing)) (an intermediary file containing information for how the file is split)
2) Passes the cuesheet to `FFmpeg` (see **Requirements** section), which performs the split
3) Outputs the tracks to directory with the format: `f"{artist}_{album}_tracksplit"` - where 'artist' and 'album' are user-provided (see **Usage** section)

If you're curious, feel free to inspect the `tracksplit.py` docstrings, for more insight into my workflow. 

I've also included some 'legacy' functions which didn't make the cut, but I think are interesting anyway, in the `Archive` folder.

## Future
FFmpeg is actually way more capable than just processing audio files. For this reason, I have planned video splitting capabilities for a future release (see `TODO.md` for more).
# Usage
```shell
./tracksplit.py --timestamps 'timestamps.txt' 
                --audio 'concert_audio.mp3'
                --artist 'Sensible Clown Conglomerate'
                --album 'The Light Side of the Sun'
```

* `--timestaps`: takes a text file containing 'YouTube style' timestamps 
* `--audio`: takes the source audio file to be split into individual tracks
* `--artist` and `--album`: respective 'artist' and 'album' metadata will be embedded during splitting process
* `--only-cue`: provided, to bypass FFmpeg, and obtain the cue sheet file for your own audio splitting workflow (see **Alternative workflows** section)

# Requirements
There are a whopping **2** ***(two)*** dependencies for core audio splitting process:
1) `FFmpeg` - a multimedia framework which [in their own words](https://ffmpeg.org/about.html) can handle 'pretty much anything that humans and machines have created'
2) `ffcuesplitter` - and a Python package which interfaces the with FFmpeg, using a source audio file specific cue sheet, generated during the pipeline   

**HOWEVER**, if you just want an audio source-file specific cue file you can BYPASS these two dependencies entirely, by providing the argument: `--only-cue`

## [FFmpeg](https://ffmpeg.org/)
If you're on macOS *and* use `homebrew`:
```shell
brew install ffmpeg
``` 
Since we're using Python, `conda` installation:
```shell
conda install -c conda-forge ffmpeg
```
Otherwise, official platform-specific installations on [FFmpeg's website](https://ffmpeg.org/download.html).

## [ffcuespliter](https://pypi.org/project/ffcuesplitter/)

Python dependency that interfaces with FFmpeg for the splitting process. See the official [repo](https://github.com/jeanslack/FFcuesplitter) for more info on how it interfaces with FFmpeg. 

Install through `pip`:
```shell
python3 -m pip install ffcuesplitter 
```

# Alternative workflows
Apart form FFmpeg, there are other cue-sheet based ways to split the audio track:
- [mp3splt](https://github.com/mp3splt/mp3splt) - frame-accurate splitting of mp3, ogg vorbis, FLAC and other audio formats without requiring decoding or re-encoding. 
- [CUEtools](https://github.com/gchudov/cuetools.net) - a tool for lossless audio/CUE sheet format conversion
- [foobar2000](https://www.foobar2000.org/) - one can use the '[Converter](https://wiki.hydrogenaud.io/index.php?title=Foobar2000:Converter)' component to split the source audio file, by dragging the respective cue file into foobar2000, highlighting, right-clicking and selecting 'Convert'