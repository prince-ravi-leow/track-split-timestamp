# Python-based tool for audio file track splitting

The purpose of this program is to provide a convenient way to perform audio file track-splitting, using simple 'YouTube style' timestamps 

E.g.
```
00:55:45 Pink Elephants on Parade
01:20:54 Circle of Life
02:54:01 Colours of the Wind
```
**An FFmpeg installation is required for the actual track splitting (see 'Requirements' section)** 

Apart from FFmpeg itself, the entire track-splitting pipeline requires a single Python dependency ([FFcuesplitter](https://pypi.org/project/ffcuesplitter/)). **HOWEVER**, should one desire to perform the actual track split with a software of their choice, one can obtain a source audio file-specific cue sheet by providing setting the `--only-cue` to `True`, which will BYPASS FFmpeg and FFcuesplitter entirely.

# Usage example
```shell
./tracksplit.py --timestamps 'timestamps.txt' 
                --audio 'concert_audio.mp3'
                --artist 'Sensible Clown Conglomerate'
                --album 'The Light Side of the Sun'
```

* `--timestaps`: takes a text file containing 'YouTube style' timestamps 
* `--audio`: takes the source audio file to be split into individual tracks
* `--artist` and `--album`: respective 'artist' and 'album' metadata will be embedded during splitting process
* `--only-cue True`: provided, to bypass FFmpeg, and obtain the cue sheet file for your own audio splitting workflow (see **Alternative workflows** section)

# Requirements
* [FFmpeg](https://ffmpeg.org/)

*Why FFmpeg?* Well, in their [own words](https://ffmpeg.org/about.html), FFmpeg is a multimedia framework, capable of converting 'pretty much anything that humans and machines have created'.

Official platform-specific installations on [FFmpeg's website](https://ffmpeg.org/download.html).

If you're on macOS and use `homebrew`:
```shell
brew install ffmpeg
``` 

* [ffcuespliter](https://github.com/jeanslack/FFcuesplitter)

Python dependency that interfaces with FFmpeg for the splitting process.
```python
python3 -m pip install ffcuesplitter 
```

# Alternative workflows
Apart form FFmpeg, there are other cue-sheet based ways to split the audio track:
- [mp3splt](https://github.com/mp3splt/mp3splt) - frame-accurate splitting of mp3, ogg vorbis, FLAC and other audio formats without requiring decoding or re-encoding. 
- [CUEtools](https://github.com/gchudov/cuetools.net) - a tool for lossless audio/CUE sheet format conversion
- [foobar2000](https://www.foobar2000.org/) - one can use the '[Converter](https://wiki.hydrogenaud.io/index.php?title=Foobar2000:Converter)' component to split the source audio file, by dragging the respective cue file into foobar2000, highlighting, right-clicking and selecting 'Convert' 

# Roadmap
I created this script, because of my personal hobby of taking concert audio, and packaging it into tracks, so that I could listen to it as an 'album'. 

This script basically uses cue sheets to accomplish this. However, due FFmpeg's flexibility, this functioanlity could easily be expanded to video.

This is planned for a future release.