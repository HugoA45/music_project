import os
import glob
import numpy as np
import pickle
from tqdm import tqdm
import miditoolkit
from pathlib import Path



# parameters for input
DEFAULT_VELOCITY_BINS = np.array([ 0, 32, 48, 64, 80, 96, 128])     # np.linspace(0, 128, 32+1, dtype=np.int)
DEFAULT_FRACTION = 16
DEFAULT_DURATION_BINS = np.arange(60, 3841, 60, dtype=int)
DEFAULT_TEMPO_INTERVALS = [range(30, 90), range(90, 150), range(150, 210)]

# parameters for output
DEFAULT_RESOLUTION = 480
# utils.py components
class Item(object):
    # ... (include the entire definition of Item class from utils.py)
    def __init__(self, name, start, end, velocity, pitch, Type):
            self.name = name
            self.start = start
            self.end = end
            self.velocity = velocity
            self.pitch = pitch
            self.Type = Type
def read_items(file_path):
    # ... (include the entire function body from utils.py)
    midi_obj = miditoolkit.midi.parser.MidiFile(file_path)
    # note
    note_items = []
    num_of_instr = len(midi_obj.instruments)

    for i in range(num_of_instr):
        notes = midi_obj.instruments[i].notes
        notes.sort(key=lambda x: (x.start, x.pitch))

        for note in notes:
            note_items.append(Item(
                name='Note',
                start=note.start,
                end=note.end,
                velocity=note.velocity,
                pitch=note.pitch,
                Type=i))

    note_items.sort(key=lambda x: x.start)

    # tempo
    tempo_items = []
    for tempo in midi_obj.tempo_changes:
        tempo_items.append(Item(
            name='Tempo',
            start=tempo.time,
            end=None,
            velocity=None,
            pitch=int(tempo.tempo),
            Type=-1))
    tempo_items.sort(key=lambda x: x.start)

    # expand to all beat
    max_tick = tempo_items[-1].start
    existing_ticks = {item.start: item.pitch for item in tempo_items}
    wanted_ticks = np.arange(0, max_tick+1, DEFAULT_RESOLUTION)
    output = []
    for tick in wanted_ticks:
        if tick in existing_ticks:
            output.append(Item(
                name='Tempo',
                start=tick,
                end=None,
                velocity=None,
                pitch=existing_ticks[tick],
                Type=-1))
        else:
            output.append(Item(
                name='Tempo',
                start=tick,
                end=None,
                velocity=None,
                pitch=output[-1].pitch,
                Type=-1))
    tempo_items = output
    return note_items, tempo_items


def item2event(groups, task):
    # ... (include the entire function body from utils.py)
    events = []
    n_downbeat = 0
    for i in range(len(groups)):
        if 'Note' not in [item.name for item in groups[i][1:-1]]:
            continue
        bar_st, bar_et = groups[i][0], groups[i][-1]
        n_downbeat += 1
        new_bar = True

        for item in groups[i][1:-1]:
            if item.name != 'Note':
                continue
            note_tuple = []

            # Bar
            if new_bar:
                BarValue = 'New'
                new_bar = False
            else:
                BarValue = "Continue"
            note_tuple.append(events(
                name='Bar',
                time=None,
                value=BarValue,
                text='{}'.format(n_downbeat),
                Type=-1))

            # Position
            flags = np.linspace(bar_st, bar_et, DEFAULT_FRACTION, endpoint=False)
            index = np.argmin(abs(flags-item.start))
            note_tuple.append(events(
                name='Position',
                time=item.start,
                value='{}/{}'.format(index+1, DEFAULT_FRACTION),
                text='{}'.format(item.start),
                Type=-1))

            # Pitch
            velocity_index = np.searchsorted(DEFAULT_VELOCITY_BINS, item.velocity, side='right') - 1

            if task == 'melody':
                pitchType = item.Type
            elif task == 'velocity':
                pitchType = velocity_index
            else:
                pitchType = -1

            note_tuple.append(events(
                name='Pitch',
                time=item.start,
                value=item.pitch,
                text='{}'.format(item.pitch),
                Type=pitchType))

            # Duration
            duration = item.end - item.start
            index = np.argmin(abs(DEFAULT_DURATION_BINS-duration))
            note_tuple.append(events(
                name='Duration',
                time=item.start,
                value=index,
                text='{}/{}'.format(duration, DEFAULT_DURATION_BINS[index]),
                Type=-1))

            events.append(note_tuple)
    return events


def quantize_items(items, ticks=120):
    # ... (include the entire function body from utils.py)
    grids = np.arange(0, items[-1].start, ticks, dtype=int)
    # process
    for item in items:
        index = np.argmin(abs(grids - item.start))
        shift = grids[index] - item.start
        item.start += shift
        item.end += shift
    return items
def group_items(items, max_time, ticks_per_bar=480*4):
    # ... (include the entire function body from utils.py)
    items.sort(key=lambda x: x.start)
    downbeats = np.arange(0, max_time+ticks_per_bar, ticks_per_bar)
    groups = []
    for db1, db2 in zip(downbeats[:-1], downbeats[1:]):
        insiders = []
        for item in items:
            if (item.start >= db1) and (item.start < db2):
                insiders.append(item)
        overall = [db1] + insiders + [db2]
        groups.append(overall)
    return groups
# model.py components (simplified for composer task)
class CP(object):
    # ... (include the entire definition of CP class from model.py)
    def __init__(self, dict):
        # load dictionary
        self.event2word, self.word2event = pickle.load(open(dict, 'rb'))
        # pad word: ['Bar <PAD>', 'Position <PAD>', 'Pitch <PAD>', 'Duration <PAD>']
        self.pad_word = [self.event2word[etype]['%s <PAD>' % etype] for etype in self.event2word]

    def extract_events(self, input_path, task):
        note_items, tempo_items = read_items(input_path)
        if len(note_items) == 0:   # if the midi contains nothing
            return None
        note_items = quantize_items(note_items)
        max_time = note_items[-1].end
        items = tempo_items + note_items

        groups = group_items(items, max_time)
        events = item2event(groups, task)
        return events

    def padding(self, data, max_len, ans):
        pad_len = max_len - len(data)
        for _ in range(pad_len):
            if not ans:
                data.append(self.pad_word)
            else:
                data.append(0)

        return data

    def prepare_data(self, midi_paths, task, max_len):
        all_words, all_ys = [], []

        for path in tqdm(midi_paths):
            # extract events
            events = self.extract_events(path, task)
            if not events:  # if midi contains nothing
                print(f'skip {path} because it is empty')
                continue
            # events to words
            words, ys = [], []
            for note_tuple in events:
                nts, to_class = [], -1
                for e in note_tuple:
                    e_text = '{} {}'.format(e.name, e.value)
                    nts.append(self.event2word[e.name][e_text])
                    if e.name == 'Pitch':
                        to_class = e.Type
                words.append(nts)
                if task == 'melody' or task == 'velocity':
                    ys.append(to_class+1)

            # slice to chunks so that max length = max_len (default: 512)
            slice_words, slice_ys = [], []
            for i in range(0, len(words), max_len):
                slice_words.append(words[i:i+max_len])
                if task == "composer":
                    name = path.split('/')[-2]
                    slice_ys.append(Composer[name])

            # padding or drop
            if len(slice_words[-1]) < max_len:
                if task == 'composer' and len(slice_words[-1]) < max_len//2:
                    slice_words.pop()
                    slice_ys.pop()
                else:
                    slice_words[-1] = self.padding(slice_words[-1], max_len, ans=False)

            all_words = all_words + slice_words
            all_ys = all_ys + slice_ys

        all_words = np.array(all_words)
        all_ys = np.array(all_ys)

        return all_words, all_ys

# Main processing function
def process_midi_files(input_dir, dict_path, max_len=512):
    model = CP(dict_path)

    all_words, all_ys = [], []
    composer_dirs = glob.glob(os.path.join(input_dir, '*'))

    for dir in tqdm(composer_dirs):
        composer_name = Path(dir).stem
        midi_files = glob.glob(os.path.join(dir, '*.mid'))
        # Pass "composer" as the task argument
        words, ys = model.prepare_data(midi_files, "composer", max_len)
        all_words.extend(words)
        all_ys.extend([Composer[composer_name]] * len(words))

    return np.array(all_words), np.array(all_ys)

# Usage example
input_dir = '/Users/tobiaslandgraf/code/HugoA45/music_project/music_project/Output_Dir'  # Path to the dataset directory
dict_path = '/Users/tobiaslandgraf/code/HugoA45/music_project/music_project/model/CP.pkl'  # Path to the dictionary file
max_len = 512  # Maximum sequence length

# Define your composer dictionary
Composer = {
    "Bethel": 0,
    "Clayderman": 1,
    "Einaudi": 2,
    "Hancock": 3,
    "Hillsong": 4,
    "Hisaishi": 5,
    "Ryuichi": 6,
    "Yiruma": 7,
    "Padding": 8,
}

# Process the MIDI files
all_words, all_ys = process_midi_files(input_dir, dict_path, max_len)

# You can now use `all_words` and `all_ys` for your machine learning tasks
print(all_words,all_ys)
