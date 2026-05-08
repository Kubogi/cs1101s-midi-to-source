# CS1101S Game of Tones - MIDI to Source Pipeline

**Winner of the CS1101S Game of Tones contest (AY2025/26 Sem 1)**

A small Python pipeline that converts a MIDI file into Source code for NUS CS1101S's sound contest. The generated program plays the first 49 seconds of [Lagtrain by inabakumori](https://www.youtube.com/watch?v=UnIhRpIT7nc), reconstructed entirely from MIDI data.

Full write-up: [Using Python to Win a JavaScript Contest](https://kubogi.github.io/2026/01/06/cs1101s-sound.html)

---

## How it works

1. **`main.py`** — reads `lagtrain_cut.mid`, pairs `note_on`/`note_off` MIDI events to reconstruct notes with start times and durations, and outputs Source-compatible function calls
2. **`output.txt`, `test.txt`, `tmp.txt`** — the intermediate generated code (one note/event per line), useful for inspecting the pipeline output before running in Source
3. **`lagtrain_source.js`** — the final Source program, ready to run in the CS1101S Source Academy environment

---

## Repo structure

```
├── main.py                 # MIDI parser and code generator
├── lagtrain_cut.mid        # MIDI source file (cut to 49s)
├── output.txt              # Intermediate generated output
├── test.txt, tmp.txt       # leftover scratch files from development
└── lagtrain_source.js      # Final Source program
```

---

## Quickstart

**Requirements:** Python 3, [MidiFile](https://pypi.org/project/MIDIFile/)

```bash
pip install MidiFile
python main.py
```

Output is written to `output.txt`. The final Source code in `lagtrain_source.js` was assembled from this output with hand-written instrument definitions.

---

## Notes

This pipeline is Lagtrain-specific. A few things are hardcoded:

- Each MIDI track has slightly different parsing logic (note grouping, chord reconstruction, percussion handling). This is currently switched manually by commenting/uncommenting blocks rather than being parameterized.
- Instrument definitions (waveforms, ADSR envelopes) are tuned by hand for this song.
- The chord mappings are specific to Lagtrain's harmonic structure.

A more general version would define a config per track and separate instrument definitions from the parser.

---

## Performance

The generated Source program loads in ~15 seconds and plays back smoothly without noticeable lag, well within the contest's practical limits.