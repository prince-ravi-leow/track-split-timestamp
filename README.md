# Python-based tool for audio file track splitting
The purpose of this program is to provide a convenient way to perform audio file track-splitting, using simple 'YouTube style' timestamps. 

E.g.
```
00:55:45 Pink Elephants on Parade
01:20:54 Circle of Life
02:54:01 Colours of the Wind
```

I created this script, because of my personal hobby of taking concert audio, and splitting it into tracks, so that I could re-package and enjoy it as an 'album'. 

# Usage
```
usage: tracksplit.py [-h] [--artist ARTIST] [--album ALBUM] [--only-cue]
                     timestamps audio

The purpose of this program is: given an existing FFmpeg installation, to split a source audio file using provided 'YouTube style' timestamps e.g.: 

00:55:45 Pink Elephants on Parade
01:20:54 Circle of Life
02:54:01 Colours of the Wind

positional arguments:
  timestamps       File containing timestamps
  audio            Audio file source

options:
  -h, --help       show this help message and exit
  --artist ARTIST  Artist name
  --album ALBUM    Album name
  --only-cue       Optional: Output cue file without performing split, when supplied
                   with 'True' argument (Default: False)
```

# Installation
## The easiest way
If you use `conda` / `mamba`:
```sh
conda env create --file env.yml
```
## Manual installation
### Install ffmpeg
If you're on macOS *and* use `homebrew`:
```shell
brew install ffmpeg
``` 
Otherwise, official platform-specific installations on [FFmpeg's website](https://ffmpeg.org/download.html).
### Install ffcuesplitter
Install through `pip`:
```shell
python3 -m pip install ffcuesplitter 
``` 

## Why these dependencies?
1) [FFmpeg](https://ffmpeg.org/) - a multimedia framework which [in their own words](https://ffmpeg.org/about.html) can handle 'pretty much anything that humans and machines have created'
2) [ffcuespliter](https://pypi.org/project/ffcuesplitter/) - and a Python package which interfaces the with FFmpeg, using a source audio file specific cue sheet, generated during the pipeline. See the official [repo](https://github.com/jeanslack/FFcuesplitter) for more info on how it interfaces with FFmpeg. 

# Alternative workflows
Apart form FFmpeg, there are other cue-sheet based ways to split the audio track:
- [mp3splt](https://github.com/mp3splt/mp3splt) - frame-accurate splitting of mp3, ogg vorbis, FLAC and other audio formats without requiring decoding or re-encoding. 
- [CUEtools](https://github.com/gchudov/cuetools.net) - a tool for lossless audio/CUE sheet format conversion
- [foobar2000](https://www.foobar2000.org/) - one can use the '[Converter](https://wiki.hydrogenaud.io/index.php?title=Foobar2000:Converter)' component to split the source audio file, by dragging the respective cue file into foobar2000, highlighting, right-clicking and selecting 'Convert'
