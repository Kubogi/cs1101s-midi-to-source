from mido import MidiFile

def midi_to_notes(path, cutoff=49.0):
    mid = MidiFile(path)
    ticks_per_beat = mid.ticks_per_beat

    # If tempo is defined in MIDI, grab it. Otherwise assume 500000 microsec/beat (120 bpm).
    tempo = 500000
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break

    print('tempo=',tempo)

    seconds_per_tick = tempo / 1_000_000 / ticks_per_beat

    notes = []
    active_notes = {}  # note -> (start_time in sec)
    absolute_time = 0  # in ticks

    last_start = 0
    last_dur = 0
    mn = 100

    tmp = []

    for (i, msg) in enumerate(mid.tracks[6]):  # take first track for now
        absolute_time += msg.time
        current_time = absolute_time * seconds_per_tick

        if current_time > cutoff:
            break  # stop reading beyond cutoff

        if msg.type == 'note_on' and msg.velocity > 0:
            # start note
            active_notes[msg.note] = current_time

        elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
            # end note
            if msg.note in active_notes:
                start = active_notes.pop(msg.note)
                dur = current_time - start
                # cut duration if note extends beyond cutoff
                if start < cutoff:
                    end_time = min(current_time, cutoff)

                    mn = min(mn, msg.note)
                    
                    # piano
                    if i % 4 == 0:
                        print(i, mn)
                        # chord = {
                        #     38: [38,42,47,50],
                        #     42: [42,47,50,54],
                        #     43: [43,48,52,75],
                        #     47: [47,51,54,57]
                        # }
                        notes.append(f'c{mn}({start - last_start - last_dur}, {end_time - start}),')
                        last_start = start
                        last_dur = end_time - start
                        mn = 100
                        
                    # notes.append(f'note(bass_guitar_note, event({msg.note}, {start - last_start - last_dur}, {end_time - start})),')
                    # last_start = start
                    # last_dur = end_time - start

                    # percussion
                    if msg.note in [27, 38, 49, 44, 46]:
                        tmp.append((msg.note, start, end_time - start))
                        # notes.append(f'note(percussion, event({msg.note}, {start - last_start - last_dur}, {end_time - start})),')
                    last_start = start
                    last_dur = end_time - start
                    
                    # notes.append({
                    #     "note": msg.note,
                    #     "start": start,
                    #     "duration": end_time - start
                    # })

    last_start = 0
    last_dur = 0
    delay = 0
    cur = []
    for (i, e) in enumerate(tmp):
        #notes.append('on:'+str(e)+f',{last_start},{last_dur}')
        e1 = e
        if len(cur) > 0:
            if abs(e[1] - cur[0][1]) > 0.01:
                if len(cur) > 1:
                    notes.append('simultaneously(list(')
                    for (j, e) in enumerate(cur):
                        notes.append(f'note(percussion, event({e[0]}, {e[1] - delay}, {e[2]}))' + ('' if j == len(cur)-1 else ','))
                        #notes.append(e)
                    notes.append(')),')
                else:
                    notes.append(f'note(percussion, event({cur[0][0]}, {cur[0][1] - delay}, {cur[0][2]})),')
                    #notes.append(e)
                
                delay = 0
                for e in cur:
                    delay = max(delay, e[1] + e[2])
                cur = []
        cur.append(e1)
        #notes.append('after:'+ str(cur))

    if len(cur) > 1:
        notes.append('simultaneously(list(')
        for (j, e) in enumerate(cur):
            notes.append(f'note(percussion, event({e[0]}, {e[1] - delay}, {e[2]}))' + ('' if j == len(cur)-1 else ','))
        notes.append(')),')
    else:
        notes.append(f'note(percussion, event({e[0]}, {e[1] - delay}, {e[2]})),')
    cur = []        
            
    return notes

# Example usage
events = midi_to_notes("lagtrain_cut.mid", cutoff=49.0)
#print(events)
with open('output.txt', 'w') as f:
    for e in events:  
        f.write(str(e))
        f.write('\n')
