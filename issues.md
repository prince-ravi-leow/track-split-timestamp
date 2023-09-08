* Running tracksplit.py will sometimes result in a 'dry run', where no output is created, except for creating a new output file. The second run seems to work reliably, as intended. 
* Possible issue with `if not only_cue:` block
Filetype is parsed with line:
```py
file_type = audio_file.split(".")[-1]
```
Which might break for `.wav` files - will have to be tested to verify.