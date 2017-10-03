import io
import random
import string
import collections
from contextlib import contextmanager
import numpy as np
from copy import deepcopy


MIDI_pitch = {
    ",,,C": 0, ",,,,B#": 0, "C3": 0, "B#4": 0, ",,,C#": 1, ",,,Db": 1, "C#3": 1, "Db3": 1, ",,,D": 2, "D3": 2,
    ",,,D#": 3, ",,,Eb": 3, "D#3": 3, "Eb3": 3, ",,,E": 4, ",,,Fb": 4, "E3": 4, "Fb3": 4, ",,,F": 5, ",,,E#": 5,
    "F3": 5, "E#3": 5, ",,,F#": 6, ",,,Gb": 6, "F#3": 6, "Gb3": 6, ",,,G": 7, "G3": 7, ",,,G#": 8, ",,,Ab": 8,
    "G#3": 8, "Ab3": 8, ",,,A": 9, "A3": 9, ",,,A#": 10, ",,,Bb": 10, "A#3": 10, "Bb3": 10, ",,,B": 11,
    ",,Cb": 11, "B3": 11, "Cb2": 11, ",,C": 12, ",,,B#": 12, "C2": 12, "B#3": 12, ",,C#": 13, ",,Db": 13,
    "C#2": 13, "Db2": 13, ",,D": 14, "D2": 14, ",,D#": 15, ",,Eb": 15, "D#2": 15, "Eb2": 15, ",,E": 16,
    ",,Fb": 16, "E2": 16, "Fb2": 16, ",,F": 17, ",,E#": 17, "F2": 17, "E#2": 17, ",,F#": 18, ",,Gb": 18,
    "F#2": 18, "Gb2": 18, ",,G": 19, "G2": 19, ",,G#": 20, ",,Ab": 20, "G#2": 20, "Ab2": 20, ",,A": 21,
    "A2": 21, ",,A#": 22, ",,Bb": 22, "A#2": 22, "Bb2": 22, ",,B": 23, ",Cb": 23, "B2": 23, "Cb1": 23, ",C": 24,
    ",,B#": 24, "C1": 24, "B#2": 24, ",C#": 25, ",Db": 25, "C#1": 25, "Db1": 25, ",D": 26, "D1": 26, ",D#": 27,
    ",Eb": 27, "D#1": 27, "Eb1": 27, ",E": 28, ",Fb": 28, "E1": 28, "Fb1": 28, ",F": 29, ",E#": 29, "F1": 29,
    "E#1": 29, ",F#": 30, ",Gb": 30, "F#1": 30, "Gb1": 30, ",G": 31, "G1": 31, ",G#": 32, ",Ab": 32, "G#1": 32,
    "Ab1": 32, ",A": 33, "A1": 33, ",A#": 34, ",Bb": 34, "A#1": 34, "Bb1": 34, ",B": 35, "Cb": 35, "B1": 35,
    "Cb0": 35, "C": 36, ",B#": 36, "C0": 36, "B#1": 36, "C#": 37, "Db": 37, "C#0": 37, "Db0": 37, "D": 38,
    "D0": 38, "D#": 39, "Eb": 39, "D#0": 39, "Eb0": 39, "E": 40, "Fb": 40, "E0": 40, "Fb0": 40, "F": 41,
    "E#": 41, "F0": 41, "E#0": 41, "F#": 42, "Gb": 42, "F#0": 42, "Gb0": 42, "G": 43, "G0": 43, "G#": 44,
    "Ab": 44, "G#0": 44, "Ab0": 44, "A": 45, "A0": 45, "A#": 46, "Bb": 46, "A#0": 46, "Bb0": 46, "B": 47,
    "cb": 47, "B0": 47, "cb0": 47, "c": 48, "B#": 48, "c0": 48, "B#0": 48, "c#": 49, "db": 49, "c#0": 49,
    "db0": 49, "d": 50, "d0": 50, "d#": 51, "eb": 51, "d#0": 51, "eb0": 51, "e": 52, "fb": 52, "e0": 52,
    "fb0": 52, "f": 53, "e#": 53, "f0": 53, "e#0": 53, "f#": 54, "gb": 54, "f#0": 54, "gb0": 54, "g": 55,
    "g0": 55, "g#": 56, "ab": 56, "g#0": 56, "ab0": 56, "a": 57, "a0": 57, "a#": 58, "bb": 58, "a#0": 58,
    "bb0": 58, "b": 59, "cb'": 59, "b0": 59, "cb1": 59, "c'": 60, "b#": 60, "c1": 60, "b#0": 60, "c#'": 61,
    "db'": 61, "c#1": 61, "db1": 61, "d'": 62, "d1": 62, "d#'": 63, "eb'": 63, "d#1": 63, "eb1": 63, "e'": 64,
    "fb'": 64, "e1": 64, "fb1": 64, "f'": 65, "e#'": 65, "f1": 65, "e#1": 65, "f#'": 66, "gb'": 66, "f#1": 66,
    "gb1": 66, "g'": 67, "g1": 67, "g#'": 68, "ab'": 68, "g#1": 68, "ab1": 68, "a'": 69, "a1": 69, "a#'": 70,
    "bb'": 70, "a#1": 70, "bb1": 70, "b'": 71, "cb''": 71, "b1": 71, "cb2": 71, "c''": 72, "b#'": 72, "c2": 72,
    "b#1": 72, "c#''": 73, "db''": 73, "c#2": 73, "db2": 73, "d''": 74, "d2": 74, "d#''": 75, "eb''": 75,
    "d#2": 75, "eb2": 75, "e''": 76, "fb''": 76, "e2": 76, "fb2": 76, "f''": 77, "e#''": 77, "f2": 77,
    "e#2": 77, "f#''": 78, "gb''": 78, "f#2": 78, "gb2": 78, "g''": 79, "g2": 79, "g#''": 80, "ab''": 80,
    "g#2": 80, "ab2": 80, "a''": 81, "a2": 81, "a#''": 82, "bb''": 82, "a#2": 82, "bb2": 82, "b''": 83,
    "cb'''": 83, "b2": 83, "cb3": 83, "c'''": 84, "b#''": 84, "c3": 84, "b#2": 84, "c#'''": 85, "db'''": 85,
    "c#3": 85, "db3": 85, "d'''": 86, "d3": 86, "d#'''": 87, "eb'''": 87, "d#3": 87, "eb3": 87, "e'''": 88,
    "fb'''": 88, "e3": 88, "fb3": 88, "f'''": 89, "e#'''": 89, "f3": 89, "e#3": 89, "f#'''": 90, "gb'''": 90,
    "f#3": 90, "gb3": 90, "g'''": 91, "g3": 91, "g#'''": 92, "ab'''": 92, "g#3": 92, "ab3": 92, "a'''": 93,
    "a3": 93, "a#'''": 94, "bb'''": 94, "a#3": 94, "bb3": 94, "b'''": 95, "cb''''": 95, "b3": 95, "cb4": 95,
    "c''''": 96, "b#'''": 96, "c4": 96, "b#3": 96, "c#''''": 97, "db''''": 97, "c#4": 97, "db4": 97,
    "d''''": 98, "d4": 98, "d#''''": 99, "eb''''": 99, "d#4": 99, "eb4": 99, "e''''": 100, "fb''''": 100,
    "e4": 100, "fb4": 100, "f''''": 101, "e#''''": 101, "f4": 101, "e#4": 101, "f#''''": 102, "gb''''": 102,
    "f#4": 102, "gb4": 102, "g''''": 103, "g4": 103, "g#''''": 104, "ab''''": 104, "g#4": 104, "ab4": 104,
    "a''''": 105, "a4": 105, "a#''''": 106, "bb''''": 106, "a#4": 106, "bb4": 106, "b''''": 107, "cb'''''": 107,
    "b4": 107, "cb5": 107, "c'''''": 108, "b#''''": 108, "c5": 108, "b#4": 108, "c#'''''": 109, "db'''''": 109,
    "c#5": 109, "db5": 109, "d'''''": 110, "d5": 110, "d#'''''": 111, "eb'''''": 111, "d#5": 111, "eb5": 111,
    "e'''''": 112, "fb'''''": 112, "e5": 112, "fb5": 112, "f'''''": 113, "e#'''''": 113, "f5": 113, "e#5": 113,
    "f#'''''": 114, "gb'''''": 114, "f#5": 114, "gb5": 114, "g'''''": 115, "g5": 115, "g#'''''": 116,
    "ab'''''": 116, "g#5": 116, "ab5": 116, "a'''''": 117, "a5": 117, "a#'''''": 118, "bb'''''": 118,
    "a#5": 118, "bb5": 118, "b'''''": 119, "cb''''''": 119, "b5": 119, "cb6": 119, "c''''''": 120,
    "b#'''''": 120, "c6": 120, "b#5": 120, "c#''''''": 121, "db''''''": 121, "c#6": 121, "db6": 121,
    "d''''''": 122, "d6": 122, "d#''''''": 123, "eb''''''": 123, "d#6": 123, "eb6": 123, "e''''''": 124,
    "fb''''''": 124, "e6": 124, "fb6": 124, "f''''''": 125, "e#''''''": 125, "f6": 125, "e#6": 125,
    "f#''''''": 126, "gb''''''": 126, "f#6": 126, "gb6": 126, "g''''''": 127, "g6": 127
}


def min_pitch():
    return min(MIDI_pitch.values())


def max_pitch():
    return max(MIDI_pitch.values())


def pitch_range():
    return np.array(range(min_pitch(), max_pitch() + 1))


def to_MIDI_pitch(pitch):
    """map to midi pitch"""
    if isinstance(pitch, (int, np.int_)):
        return int(pitch)
    elif isinstance(pitch, str):
        try:
            pitch = int(pitch)
        except ValueError:
            return MIDI_pitch[pitch]
        return pitch
    else:
        raise UserWarning("Cannot interpret '{}' (type {}) as pitch".format(pitch, type(pitch)))


@contextmanager
def transposed(event, transpose_event):
    event._transpose_list += [(transpose_event._transpose, transpose_event._scale)]
    event._transpose_list += transpose_event._transpose_list
    yield
    event._transpose_list = event._transpose_list[:-1-len(transpose_event._transpose_list)]


def metrical_grid(nested_idx):
    """
    Returns the depth inside the metrical grid
    :param nested_idx: nested index on grid levels
    :return: depth

    For a 4/4 measure:
    |
    |       |
    |   |   |   |
    | | | | | | | |
    0 3 2 3 1 3 2 3 (depth)
    -----------------------
    0 0 0 0 0 0 0 0 (nested
    0 0 0 0 1 1 1 1  ...
    0 0 1 1 0 0 1 1  ...
    0 1 0 1 0 1 0 1  index)

    For a 12/8 measure:
    |
    |           |
    |     |     |     |
    | | | | | | | | | | | |
    0 3 3 2 3 3 1 3 3 2 3 3 (depth)
    -------------------------------
    0 0 0 0 0 0 0 0 0 0 0 0 (nested
    0 0 0 0 0 0 1 1 1 1 1 1  ...
    0 0 0 1 1 1 0 0 0 1 1 1  ...
    0 1 2 0 1 2 0 1 2 0 1 2  index)
    """
    idx = 0
    for idx, n_idx in reversed(list(enumerate(nested_idx))):
        if n_idx > 0:
            break
    return idx


def repack_list(list_to_repack, package_sizes=()):
    if not package_sizes:
        return list_to_repack
    repacked_list = []
    while list_to_repack:
        package = []
        for idx in range(package_sizes[0]):
            package.append(list_to_repack[0])
            list_to_repack = list_to_repack[1:]
            if not list_to_repack:
                break
        repacked_list.append(package)
    package_sizes = package_sizes[1:]
    return repack_list(repacked_list, package_sizes)


def rotate(intervals, n):
    intervals = list(intervals)
    rot = n % len(intervals)
    shift = n // len(intervals)
    octaves = 1 + (max(intervals) - min(intervals)) // 12
    rotated_intervals = intervals[rot:] + [i + 12 * octaves for i in intervals[:rot]]
    return [i + 12 * shift for i in rotated_intervals]


@contextmanager
def write_song(file=None, print_to_std_out=False, add_code=""):
    Event.reset()
    with io.StringIO() as content:
        print("# additional code", file=content)
        print(add_code, file=content)
        print("", file=content)
        Event._output_file = content
        print("# main function", file=content)
        print("def song", file=content)
        Event._indent += 1
        yield
        Event._indent -= 1
        print("end", file=content)
        print("", file=content)
        Event.write_loops(content)
        print("", file=content)
        Event.write_symbols(content)
        if print_to_std_out:
            print(content.getvalue())
        if file is not None:
            with open(file, 'w') as song:
                print(content.getvalue(), file=song)


class TonicScale:

    def __init__(self, tonic=None, intervals=range(12), pitches=None):
        if isinstance(intervals, str):
            if intervals == 'major':
                intervals = [0, 2, 4, 5, 7, 9, 11]
            elif intervals == 'minor':
                intervals = [0, 2, 3, 5, 7, 8, 10]
            else:
                raise UserWarning("Unknown scale '{}' given as intervals parameter".format(intervals))
        if pitches is not None:
            if tonic is None:
                self._tonic = pitches[0]
            else:
                self._tonic = tonic
            intervals = [(to_MIDI_pitch(p) - to_MIDI_pitch(pitches[0])) % 12 for p in pitches]
        else:
            self._tonic = "c'" if tonic is None else tonic
        self._intervals = np.array(sorted(np.unique(intervals)))
        if self._intervals[0] < 0:
            raise UserWarning("Scale cannot contain negative intervals.")
        if self._intervals[-1] > 11:
            raise UserWarning("Scale cannot contain intervals of an octave or above.")

    def __repr__(self):
        return str([to_MIDI_pitch(self._tonic) + i for i in self._intervals])

    def get_interval(self, scale_degree):
        return self._intervals[scale_degree % len(self._intervals)] + 12 * (scale_degree // len(self._intervals))

    def get_scale_degree(self, pitch):
        return np.argmin((self._intervals + to_MIDI_pitch(self._tonic) - to_MIDI_pitch(pitch)) % 12)

    def is_in_scale(self, pitch):
        degree = self.get_scale_degree(pitch)
        return (to_MIDI_pitch(self._tonic) + self.get_interval(degree) - to_MIDI_pitch(pitch)) % 12 == 0


class Event:

    _indent = 0
    _beat = 1
    _symbols = {}
    _loops = set()
    _str_verbose = True
    _output_file = None

    @staticmethod
    def reset():
        Event._indent = 0
        Event._beat = 1
        Event._symbols = {}
        Event._loops = set()

    @staticmethod
    def write_indent(file):
        for _ in range(Event._indent):
            print("  ", end="", file=file)

    @staticmethod
    def time_interval(extent):
        if isinstance(extent, str):
            if extent.endswith("sec"):
                # sec
                return float(extent[:-3])
            elif extent.endswith("ms"):
                # ms --> sec
                return float(extent[:-2])/1000
            elif extent.endswith("b"):
                # beats --> sec
                return float(extent[:-1]) * Event._beat
            elif '/' in extent:
                # x/y --> sec [1/4 = 1 beat]
                parts = extent.split('/')
                return 4 * float(parts[0]) / float(parts[1]) * Event._beat
            else:
                # --> sec
                return float(extent)
        else:
            # return as is
            return extent

    @staticmethod
    def set_beat(beat):
        if isinstance(beat, str):
            if beat.endswith('bpm'):
                Event._beat = float(60 / float(beat[:-3]))
            else:
                Event._beat = float(beat)
        else:
            Event._beat = beat

    @staticmethod
    def random_string(length=10, lower=True, upper=False, digits=False):
        pool = ''
        if lower:
            pool += string.ascii_lowercase
        if upper:
            pool += string.ascii_uppercase
        if digits:
            pool += string.digits
        return ''.join(random.choices(pool, k=length))

    @staticmethod
    def write_symbols(file):
        print("# symbols", file=file)
        print("", file=file)
        for function_name, function, extent in Event._symbols.values():
            print(function, file=file)
            print("", file=file)

    @staticmethod
    def write_loops(file):
        print("# function for testing infinite loops", file=file)
        print("def loop_test(key)", file=file)
        print("  loops = [", file=file)
        for name in Event._loops:
            print("    '{}',".format(name), file=file)
        print("  ].to_set", file=file)
        print("  return loops.include?(key)", file=file)
        print("end", file=file)

    @staticmethod
    def add_loop(name):
        if name in Event._loops:
            raise UserWarning("Loop '{}' already exists".format(name))
        else:
            Event._loops.add(name)

    @staticmethod
    def parse(event, agglomeration_type="Sequence"):
        if isinstance(event, str):
            # string should be single event or sequence of events separated by whitespace
            list = event.split()
            if len(list) > 1:
                # sequence
                sequence = []
                for e in list:
                    sequence.append(Event.parse(e))
                if agglomeration_type == "Sequence":
                    return Sequence(sequence)
                elif agglomeration_type == "Parallel":
                    return Parallel(sequence)
                else:
                    raise UserWarning("Unknown agglomeration type {}".format(agglomeration_type))
            else:
                # single event
                vals = event.split('/')
                length = "1b"
                if len(vals) > 1:
                    length = "1/" + vals[1]
                if vals[0] == 'r' or vals[0] == 'R':
                    return Rest(length)
                if vals[0][0:2].lower() == 'b:':
                    return Beat(length, sound=vals[0][2:])
                else:
                    pitch = vals[0]
                    tie = False
                    staccato = False
                    while pitch.endswith("_") or pitch.endswith("."):
                        if pitch.endswith("_"):
                            pitch = pitch[:-1]
                            tie = True
                        if pitch.endswith("."):
                            pitch = pitch[:-1]
                            staccato = True
                    return Tone(pitch=pitch, duration=length, tie=tie, staccato=staccato)
        else:
            # just pass through
            return event

    @staticmethod
    def wait(time, file):
        Event.write_indent(file=file)
        print("sleep {}".format(time), file=file)

    def __init__(self, transpose=0, scale=TonicScale()):
        self._transpose = transpose
        self._scale = scale
        self._transpose_list = []

    def create_symbol(self, symbol, random_name=False):
        function_name = Event.random_string() if random_name else "function_"+symbol
        with io.StringIO() as file:
            old_indent = Event._indent
            print("def {} # {}".format(function_name, symbol), file=file)
            Event._indent = 1
            self.write(file)
            print("end", end='', file=file)
            Event._indent = old_indent
            Event._symbols[symbol] = (function_name, file.getvalue(), self.extent())

    def transpose(self, trp):
        if self.is_transposable():
            self._transpose = trp
        return self

    def is_atomic(self):
        return False

    def is_transposable(self):
        return False

    def extent(self):
        return 0

    def write(self, file=None):
        pass


class Chord(Event):

    def __init__(self,
                 intervals,
                 base,
                 duration='1/4',
                 extent=None,
                 amplitude=1.,
                 symbol=None,
                 tie=False,
                 staccato=False,
                 transpose=0,
                 scale=TonicScale(),
                 synth=None):
        super(Chord, self).__init__(transpose=transpose, scale=scale)
        self._intervals = list(sorted(intervals))
        self._base = base
        self._duration = duration
        self._extent = duration if extent is None else extent
        self._amplitude = amplitude
        self._tie = tie
        self._staccato = staccato
        self._synth = synth
        if symbol is not None:
            self.create_symbol(symbol)

    def __repr__(self):
        if Event._str_verbose:
            return "Chord({}[{}]+{}{}{} {}|{} {})".format(tuple(self._intervals),
                                                             self._base,
                                                             self._transpose,
                                                             ("_" if self._tie else ""),
                                                             ("." if self._staccato else ""),
                                                             self._duration,
                                                             self._extent,
                                                             self._amplitude)
        else:
            return "{}/{}+{}:{}".format(tuple(self._intervals),
                                        self._base,
                                        self._transpose,
                                        self._duration)

    def rotate(self, n):
        self._intervals = rotate(self._intervals, n)
        if np.any(np.array(self.get_pitches()) < min_pitch()) or np.any(np.array(self.get_pitches()) > max_pitch()):
            raise UserWarning("pitches out of range: {}".format(self.get_pitches()))
        return self

    def get_pitches(self):
        return [i + to_MIDI_pitch(self._base) for i in self._intervals]

    def is_atomic(self):
        return True

    def is_transposable(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        transpose_list = [(self._transpose, self._scale)] + self._transpose_list
        duration = Event.time_interval(self._duration)
        if self._staccato:
            duration = 0.01
        for interval in self._intervals:
            pitch = to_MIDI_pitch(self._base) + interval
            for transpose, scale in transpose_list:
                scale_degree = scale.get_scale_degree(pitch=pitch)
                pitch -= scale.get_interval(scale_degree=scale_degree)
                pitch += scale.get_interval(scale_degree=scale_degree + transpose)
            if self._synth is not None:
                Event.write_indent(file)
                print("use_synth {}".format(self._synth),
                      file=file)
            Event.write_indent(file)
            print("play {}, attack: 0.01, decay: {}, sustain: 0.1, release: 0.1, amp: {}".format(pitch,
                                                                                                 duration,
                                                                                                 self._amplitude),
                  file=file)


class Tone(Chord):

    def __init__(self, pitch,
                 duration='1/4',
                 extent=None,
                 amplitude=1.,
                 symbol=None,
                 tie=False,
                 staccato=False,
                 transpose=0,
                 scale=TonicScale(),
                 synth=None):
        super(Tone, self).__init__(base=pitch,
                                   intervals=[0],
                                   duration=duration,
                                   extent=extent,
                                   amplitude=amplitude,
                                   symbol=symbol,
                                   tie=tie,
                                   staccato=staccato,
                                   transpose=transpose,
                                   scale=scale,
                                   synth=synth)

    def __repr__(self):
        if Event._str_verbose:
            return Chord.__repr__(self)
        else:
            return "{}+{}:{}".format(self._base,
                                     self._transpose,
                                     self._duration)


class Sound(Event):

    def __init__(self, sound, extent='1/4', symbol=None, add_code=""):
        super(Sound, self).__init__(transpose=0, scale=TonicScale())
        self._extent = extent
        self._sound = sound
        self._add_code = add_code
        if symbol is not None:
            self.create_symbol(symbol)

    def __repr__(self):
        return "sound:{}:{}".format(self._sound, self._extent)

    def is_atomic(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        Event.write_indent(file)
        print("sample {}{}".format(self._sound, self._add_code), file=file)

class Beat(Sound):
    """
    Possible sounds are: "snare", "tab", "kick", "hh_c", "hh_o", "ride"
    """

    sounds = {
        "snare": ":drum_snare_soft",
        "tab": ":tabla_ghe1",
        "kick": ":drum_bass_soft",
        # "kick": ":drum_heavy_kick",
        "hh_c": ":drum_cymbal_closed",
        "hh_o": ":drum_cymbal_open",
        "ride": ":drum_cymbal_hard",
        # "ride": ":drum_cymbal_soft"
    }

    def __init__(self, extent='1/4', amplitude=1., symbol=None, sound='tab'):
        sound_sconicpi = Beat.sounds[sound] if sound in Beat.sounds else ':' + sound
        super(Beat, self).__init__(sound=sound_sconicpi, extent=extent, symbol=symbol)
        self._amplitude = amplitude

    def __repr__(self):
        return "beat:{}:{},{}".format(self._sound, self._extent, self._amplitude)

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        Event.write_indent(file)
        print("sample {}, amp: {}".format(self._sound, self._amplitude), file=file)


class Rest(Event):
    def __init__(self, extent='1/4', symbol=None):
        super(Rest, self).__init__(transpose=0, scale=TonicScale())
        self._extent = extent
        if symbol is not None:
            self.create_symbol(symbol)

    def __repr__(self):
        return "r:{}".format(self._extent)

    def is_atomic(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file=None):
        pass


class Sequence(Event):

    # WARNING!!! There is a bug, this only works once. Consider this code:
    # x = ["a", "b", "c"]
    # for x in Sequence.flatten(x):
    #     print(x)
    # for x in Sequence.flatten(x):
    #     print(x)
    # for x in Sequence.flatten(x):
    #     print(x)
    @staticmethod
    def flatten(sequence):
        for event in sequence:
            if isinstance(event, collections.Iterable) and not isinstance(event, (str, bytes)):
                yield from Sequence.flatten(event)
            elif isinstance(event, Sequence):
                yield from event._sequence
            else:
                yield event

    def __init__(self, sequence, symbol=None, transpose=0, scale=TonicScale(), make_deepcopy=True):
        super(Sequence, self).__init__(transpose=transpose, scale=scale)
        # self._sequence = Sequence.flatten(sequence) # this triggers the bug from above on multiple iterations through sequence
        self._sequence = list(Sequence.flatten(sequence))
        if make_deepcopy:
            for i in range(len(self._sequence)):
                self._sequence[i] = deepcopy(self._sequence[i])
        if symbol is not None:
            self.create_symbol(symbol)

    def __repr__(self):
        s = "||["
        first = True
        for e in self._sequence:
            if first:
                first = False
            else:
                s += ", "
            s += str(e)
        s += "]"
        return s

    def is_transposable(self):
        return True

    def get_sequence(self):
        return self._sequence

    def extent(self):
        extent = 0
        for event in self._sequence:
            extent += event.extent()
        return extent

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        tie_extent = 0
        flat_sequence = list(self._sequence)
        for i in range(len(flat_sequence)):
            event = flat_sequence[i]
            if isinstance(event, Tone) \
                    and event._tie \
                    and i < len(flat_sequence) - 1 \
                    and isinstance(flat_sequence[i+1], Tone) \
                    and to_MIDI_pitch(flat_sequence[i+1]._pitch) == to_MIDI_pitch(event._pitch):
                tie_extent += event.extent()
                continue
            if tie_extent > 0:
                event._duration = tie_extent + Event.time_interval(event._duration)
                event._extent = tie_extent + Event.time_interval(event._extent)
                tie_extent = 0
            with transposed(event, self):
                event.write(file=file)
                if event.is_atomic() and event.extent() > 0:
                    Event.wait(time=event.extent(), file=file)


class Measure(Sequence):
    def __init__(self,
                 events,
                 extent,
                 unit='b',
                 symbol=None,
                 make_deepcopy=True,
                 nested_idx=(1,),
                 amplitude=lambda nested_idx: 0.05 + 0.95 * np.exp(-metrical_grid(nested_idx) / 3)):
        if isinstance(events, (str, Event)):
            e = Event.parse(events)
            if make_deepcopy:
                e = deepcopy(e)
            if e.is_atomic():
                e._extent = str(extent)+unit
            else:
                raise UserWarning("Don't know how to handle non-atomic event {} in measure".format(e))
            if isinstance(e, Chord):
                e._duration = str(extent)+unit
            if isinstance(e, (Chord, Beat)):
                e._amplitude *= amplitude(nested_idx=nested_idx)
            sequence = [e]
        else:
            sequence = []
            part_extent = extent
            if events:
                part_extent /= len(events)
            for idx, e in enumerate(events):
                sequence.append(Measure(e, part_extent, unit=unit, nested_idx=list(nested_idx) + [idx]))
        super(Measure, self).__init__(sequence, symbol=symbol, make_deepcopy=make_deepcopy)


class Parallel(Event):

    @staticmethod
    def flatten(event, onset=0):
        if event.is_atomic():
            yield (event, onset, onset + event.extent())
        elif isinstance(event, Symbol):
            raise UserWarning("Cannot parallelize Symbol event {}".format(event))
        elif isinstance(event, Loop):
            raise UserWarning("Cannot parallelize Loop event {}".format(event))
        elif isinstance(event, Parallel):
            for e in event._block:
                yield from Parallel.flatten(event=e, onset=onset)
        elif isinstance(event, Sequence):
            new_onset = onset
            for e in event.get_sequence():
                if e.extent() is not None:
                    yield from Parallel.flatten(event=e, onset=new_onset)
                    new_onset += e.extent()
                else:
                    raise UserWarning("Cannot parallelize event {} with undefined extent {}".format(e, e.extent()))
        else:
            raise UserWarning("Don't know how to handle event {} in parallelization".format(event))

    def __init__(self, block, symbol=None, transpose=0, scale=TonicScale(), make_deepcopy=True):
        super(Parallel, self).__init__(transpose=transpose, scale=scale)
        self._block = block
        if make_deepcopy:
            for i in range(len(self._block)):
                self._block[i] = deepcopy(self._block[i])
        if symbol is not None:
            self.create_symbol(symbol)

    def __repr__(self):
        s = "==["
        first = True
        for e in self._block:
            if first:
                first = False
            else:
                s += ", "
            s += str(e)
        s += "]"
        return s

    def is_transposable(self):
        return True

    def extent(self):
        extent = 0
        for event in self._block:
            extent = max(extent, event.extent())
        return extent

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        time = 0
        max_offset = 0
        for event, onset, offset in sorted(list(Parallel.flatten(self)), key=lambda x: x[1]):
            max_offset = max(max_offset, offset)
            if onset > time:
                Event.wait(time=onset - time, file=file)
                time = onset
            with transposed(event, self):
                event.write(file=file)
        if max_offset > time:
            Event.wait(time=max_offset - time, file=file)


class Transposed(Event):

    def __init__(self, event, transpose, scale=TonicScale(), make_deepcopy=False):
        super(Transposed, self).__init__(transpose=transpose, scale=scale)
        if not event.is_transposable():
            raise UserWarning("Cannot transpose event {}".format(event))
        if make_deepcopy:
            self._event = deepcopy(event)
        else:
            self._event = event

    def __repr__(self):
        return "T("+str(self._event)+", {})".format(self._transpose)

    def is_atomic(self):
        return self._event.is_atomic()

    def is_transposable(self):
        return True

    def extent(self):
        return self._event.extent()

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        with transposed(self._event, self):
            self._event.write(file)


class Symbol(Event):

    def __init__(self, symbol):
        super(Symbol, self).__init__(transpose=0, scale=TonicScale())
        self._symbol = symbol

    def extent(self):
        return Event._symbols[self._symbol][2]

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        Event.write_indent(file)
        print("{} # {}".format(Event._symbols[self._symbol][0], self._symbol), file=file)


class Loop(Event):

    def __init__(self, event, symbol=None, repeat=None, active=True, transpose=0, scale=TonicScale()):
        super(Loop, self).__init__(transpose=transpose, scale=scale)
        self._symbol = symbol if symbol is not None else Event.random_string()
        self._repeat = repeat
        with transposed(event, self):
            event.create_symbol(self._symbol)
        self._symbol_event = Symbol(self._symbol)
        if active:
            Event.add_loop(self._symbol)

    def __repr__(self):
        return "Loop("+self._symbol+")"

    def extent(self):
        if self._repeat is None:
            return None
        else:
            return self._repeat * self._symbol_event.extent()

    def write(self, file=None):
        if file is None:
                file = Event._output_file
        Event.write_indent(file)
        if self._repeat is None:
            print("while loop_test('{}')".format(self._symbol), file=file)
        else:
            print("{}.times do".format(self._repeat), file=file)
        Event._indent += 1
        Event.write_indent(file)
        print('''puts "restart {}loop '{}'"'''.format(
            ('' if self._repeat is None else "{}-time-".format(self._repeat)),
            self._symbol),
            file=file)
        self._symbol_event.write(file)
        Event._indent -= 1
        Event.write_indent(file)
        print("end", file=file)


class TimeSeriesModel:

    def __init__(self, alphabet, cache_size=1):
        self._alphabet = alphabet
        self._normalize = False
        self._cache_size = cache_size
        self._cache_keys = []
        self._cache_dict = {}

    def set_cache_size(self, cache_size):
        self._cache_size = cache_size
        while len(self._cache_keys) > self._cache_size:
            self.pop_cache()

    def pop_cache(self):
        key = self._cache_keys.pop(0)
        del self._cache_dict[key]

    def insert_in_cache(self, history_tuple, distribution):
        self._cache_keys.append(history_tuple)
        self._cache_dict[history_tuple] = distribution

    def probability(self, history, event):
        return 1 / len(self._alphabet)

    def get_distribution(self, history):
        h_tuple = tuple(history)
        if h_tuple in self._cache_dict:
            dist = self._cache_dict[h_tuple]
        else:
            dist = [self.probability(history, event) for event in self._alphabet]
            if self._normalize:
                dist = np.array(dist)
                dist /= dist.sum()
            if self._cache_size > 0:
                if len(self._cache_keys) >= self._cache_size:
                    self.pop_cache()
                self.insert_in_cache(h_tuple, dist)
        return dist

    def sample(self, history=(), steps=0, copy_history=True):
        if copy_history:
            history = list(deepcopy(history))
        for idx in range(max(steps, 1)):
            dist = self.get_distribution(history)
            try:
                history += [np.random.choice(self._alphabet, p=dist)]
            except ValueError:
                print("probabilities: {}".format(dist))
                print("sum: {}".format(np.sum(dist)))
                raise
        if steps == 0:
            return history[-1]
        else:
            return history


class FactorModel(TimeSeriesModel):

    def __init__(self, alphabet, weights=(), factors=(), weight_factors=None, cache_size=1):
        super(FactorModel, self).__init__(alphabet=alphabet, cache_size=cache_size)
        self._normalize = True
        if weight_factors is None:
            if len(factors) != len(weights):
                raise UserWarning("Unequal number of factors and weights ({}/{})".format(len(factors), len(weights)))
            self._factors = factors
            self._weights = weights
        else:
            if weights != () or factors != ():
                raise UserWarning("Cannot handle both 'weight_factors' and 'weights' and 'factors' specified separately")
            self._weights, self._factors = zip(*weight_factors)

    def log_probability(self, history, event):
        lin_comb = 0
        for f, w in zip(self._factors, self._weights):
            lin_comb += f(history, event) * w
        return lin_comb

    def probability(self, history, event):
        return np.exp(self.log_probability(history=history, event=event))


class MarkovModel(TimeSeriesModel):

    def __init__(self, alphabet, prior_counts=0):
        super(MarkovModel, self).__init__(alphabet)
        self._n_gram_counts = {}
        self._count_sums = {}
        self._normalize = True
        self._prior_counts = prior_counts

    def add_data_point(self, n_gram):
        h_tuple = tuple(n_gram)
        if h_tuple in self._n_gram_counts:
            self._n_gram_counts[h_tuple] += 1
        else:
            self._n_gram_counts[h_tuple] = 1
        if len(h_tuple) in self._count_sums:
            self._count_sums[len(h_tuple)] += 1
        else:
            self._count_sums[len(h_tuple)] = 1

    def add_history(self, history):
        for begin in range(len(history)):
            self.add_data_point(history[begin:])

    def add_sequence(self, sequence):
        for end in range(len(sequence)):
            self.add_history(sequence[0:end + 1])

    def add_corpus(self, corpus):
        for sequence in corpus:
            self.add_sequence(sequence)

    def reset_model(self):
        self._n_gram_counts = {}
        self._count_sums = {}

    def probability(self, history, event):
        for context_length in reversed(range(len(history)+1)):
            if context_length == 0:
                h_tuple = (event,)
            else:
                h_tuple = tuple(history[-context_length:] + [event])
            if h_tuple in self._n_gram_counts:
                return self._n_gram_counts[h_tuple] / self._count_sums[len(h_tuple)]
        return self._prior_counts / self._count_sums[1]

class IntervalSeries(TimeSeriesModel):

    def __init__(self, intervals, time_delay=1, epsilon=0):
        super(IntervalSeries, self).__init__([pitch for pitch in pitch_range()])
        self._intervals = np.array(intervals)
        self._time_delay = time_delay
        self._epsilon = epsilon
        self._uniform = 1 / len(self._alphabet)

    def probability(self, history, event):
        if len(history) < self._time_delay:
            return 1 / len(self._alphabet)
        else:
            shifted = (history[-self._time_delay] + self._intervals)
            in_range = len(np.nonzero(np.logical_and(min_pitch() <= shifted, max_pitch() >= shifted))[0])
            prob = 0
            if history[-self._time_delay] - event in self._intervals:
                prob += 1 / in_range
            return (1 - self._epsilon) * prob + self._epsilon * self._uniform

class TimeSeriesProduct(TimeSeriesModel):

    def __init__(self, list_of_models):
        alphabet = list(list_of_models[0]._alphabet)
        for model in list_of_models:
            if list(model._alphabet) != list(alphabet):
                raise UserWarning("Alphabets do not match:\n    {}\n    {}".format(list(model._alphabet),
                                                                                   list(alphabet)))
        super(TimeSeriesProduct, self).__init__(alphabet)
        self._list_of_models = list_of_models

    def compute_product(self, history):
        dist = []
        for e in self._alphabet:
            prob = None
            for idx, model in enumerate(self._list_of_models):
                if prob is None:
                    prob = model.probability(history, e)
                else:
                    prob *= model.probability(history, e)
            dist.append(prob)
        dist = np.array(dist)
        dist /= dist.sum()
        return dist

    def sample(self, history):
        return np.random.choice(self._alphabet, p=self.compute_product(history))

    def probability(self, history, event):
        for prob, e in zip(self.compute_product(history), self._alphabet):
            if e == event:
                return prob
        raise UserWarning("Event {} not found in alphabet {}".format(event, self._alphabet))


class PitchDistribution(TimeSeriesModel):

    def __init__(self, distribution, epsilon=0):
        super(PitchDistribution, self).__init__(pitch_range())
        distribution = np.array(distribution)
        self._distribution = (1 - epsilon) * distribution + epsilon * np.ones_like(distribution) / len(distribution)

    def sample(self, history):
        try:
            return np.random.choice(self._alphabet, p=self._distribution)
        except ValueError:
            print("probabilities: {}".format(self._distribution))
            raise

    def probability(self, history, event):
        for e, prob in zip(self._alphabet, self._distribution):
            if e == event:
                return prob
        raise UserWarning("Event {} not found in alphabet {}".format(event, self._alphabet))


class ScaleDistribution(PitchDistribution):

    def __init__(self, scale, epsilon=0):
        self._scale = scale
        distribution = np.array([(1. if self._scale.is_in_scale(pitch) else 0.) for pitch in pitch_range()])
        distribution /= distribution.sum()
        super(ScaleDistribution, self).__init__(distribution, epsilon)


class PitchRange(PitchDistribution):

    def __init__(self, min_pitch, max_pitch, epsilon=0):
        self._min_pitch = min_pitch
        self._max_pitch = max_pitch
        distribution = [
            (1 / (self._max_pitch - self._min_pitch + 1)
             if pitch >= self._min_pitch and pitch <= self._max_pitch else 0)
            for pitch in pitch_range()
            ]
        super(PitchRange, self).__init__(distribution, epsilon)


class BeamInference:

    def __init__(self, n_beams, model):
        self._n_beams = n_beams
        self._model = model
        self._beams = [[] for _ in range(n_beams)]
        self._likelihoods = [1. for _ in range(n_beams)]

    def initialize_history(self, history):
        for b in self._beams:
            b = list(history)

    def sample(self, steps=1, init_history=None, print_progress=False):
        # initialize history if requested
        if init_history is not None:
            self.initialize_history(init_history)
        # sample 'steps' steps
        for sample_idx in range(steps):
            if print_progress > 0:
                print("Sample #{}".format(sample_idx))
            n = len(self._beams)
            new_beam_list = []
            for beam_idx, (old_beam, old_likelihood) in enumerate(zip(self._beams, self._likelihoods)):
                if print_progress > 1:
                    print("    beam #{}".format(beam_idx))
                # find n most likely continuations for each of the n beams
                likely_events = sorted(
                    zip(self._model._alphabet, self._model.get_distribution(old_beam)),
                    # [(event, self._model.probability(old_beam, event)) for event in self._model._alphabet],
                    key=lambda x: x[1]
                )[-n:]
                # append new event and update likelihoods
                # (add minimal random noise for tie-breaking)
                noise = 1e-5
                for event, prob in likely_events:
                    new_beam_list.append((old_beam + [event], old_likelihood * prob * np.random.uniform(1-noise, 1)))
            # choose n most likely continuations
            self._beams = []
            self._likelihoods = []
            for beam_idx, (new_beam, new_likelihood) in enumerate(reversed(sorted(new_beam_list, key=lambda x: x[1]))):
                if new_beam not in self._beams:
                    self._beams.append(new_beam)
                    self._likelihoods.append(new_likelihood)
                if len(self._beams) == self._n_beams:
                    break
        # return most likely sequence
        return self._beams[0]


class TestModel(TimeSeriesModel):
    """A test model for beam inference where the initially most likely
    sequences don't have likely continuations after 'switch_time' steps"""

    def __init__(self, switch_time=5):
        super(TestModel, self).__init__(list(range(10)))
        self._normalize = True
        self._switch_time = switch_time

    def probability(self, history, event):
        if len(history) == 0:
            if event == 0:
                return 1.
            else:
                return 0.
        elif len(history) < self._switch_time:
            if event - history[-1] == 0:
                return 0.4
            elif event - history[-1] == 1:
                return 0.6
            else:
                return 0.
        else:
            if np.all((np.array(history) - event) == 0):
                return 1
            else:
                return 1/len(self._alphabet)


if __name__ == "__main__":
    with io.StringIO() as file:
        # create events and write to string-file
        Event.set_beat("80bpm")
        print("# main function", file=file)
        print("def song", file=file)
        Event._indent += 1
        ## measures
        m = Measure(['d', 'd', 'f', ['g_', 'g_', "d'"], 'a', 'g', 'f', 'e'], 4, 'sec') # swing
        m = Measure(['c', 'd', 'e', 'f', ['g', 'f'], ['e', 'd', 'c', 'B'], 'c'], 4)
        m = Measure([[["c'.", "d'."], ["e'.", "f'."]],
                     ["g'/2.", "g'/2."],
                     ["a'.", "a'.", "a'.", "a'."],
                     ["g'/1."],
                     ["a'.", "a'.", "a'.", "a'."],
                     ["g'/1."],
                     ["f'.", "f'.", "f'.", "f'."],
                     ["e'/2.", "e'/2."],
                     ["g'.", "g'.", "g'.", "g'."],
                     ["c'/1."]], extent=20)
        beat = Beat(extent="1/16", sound=1)
        beats = Measure([
            [[[beat, beat, beat], [beat, beat]],
             [[beat,       beat], [beat, beat]]],
            [[[beat,       beat], [beat, beat]],
             [[beat,       beat], [beat, beat]]],
            # [beat, beat, beat, beat],
        ], extent=8)
        beats = Measure([[[[[Beat(extent=1, sound='kick')] * 2] * 2] * 2] * 2], 4)
        # m.write(file)
        # Event.parse_event('r r/1').write(file)
        ## basic beat
        t = Tone("e", "1/4", amplitude=0.7)
        s = Sequence(
            [Beat(extent="1/4", amplitude=0.5),
             Parallel([t, Transposed(t, 4)]),
             Beat(extent="1/4", amplitude=1.),
             Rest("1/4")]
        )
        e = Event.parse("c r c. c. c. r c_ c_ c r")
        # print(e)
        # print(Sequence([e, f]))
        ## chords
        # print(Chord(intervals=[0, 4, 7], base="e", duration="1/4", amplitude=0.7).rotate(1))
        ##
        ## alle meine entchen
        alle_mein_entchen = Event.parse("c' d' e' f' g'/2 g'/2 a' a' a' a' g'/1 a' a' a' a' g'/1 f' f' f' f' e'/2 e'/2 g' g' g' g' c'/1")
        scale = TonicScale(tonic="c'", pitches=["c", "d", "e", "f", "g", "a", "b", "c"])
        # print(scale)
        ##
        pitchrange = PitchRange(60, 72)
        scale_dist = ScaleDistribution(scale=TonicScale(pitches=["c", "d", "e", "f", "g", "a", "b"]))
        time_series_model = TimeSeriesProduct([pitchrange, scale_dist])
        # time_series_model = TimeSeriesProduct([IntervalSeries([-1, 1]), IntervalSeries([-3, 3], 3, epsilon=0.01)])
        # rand_sequence = [60]
        # beam_inference = BeamInference(5, time_series_model)
        # rand_sequence = beam_inference.sample(steps=16 - len(rand_sequence), init_history=rand_sequence)
        markov_model = MarkovModel(pitch_range())
        # markov_model.add_corpus([[to_MIDI_pitch(pitch)] for pitch in ["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"]])
        markov_model.add_corpus([[to_MIDI_pitch(pitch) for pitch in ["c'", "d'", "e'", "f'", "g'", "g'", "a'", "a'", "a'", "a'", "g'", "a'", "a'", "a'", "a'", "g'", "f'", "f'", "f'", "f'", "e'", "e'", "g'", "g'", "g'", "g'", "c'"]]] * 100)
        print(markov_model._n_gram_counts)
        time_series_model = markov_model
        rand_sequence = [60, 62, 64, 65, 67]
        beam_inference = BeamInference(model=time_series_model, n_beams=10)
        for _ in range(16 - len(rand_sequence)):
            rand_sequence.append(time_series_model.sample(rand_sequence))
            # rand_sequence.append(beam_inference.sample(steps=1, init_history=rand_sequence)[-1])
            markov_model.add_history(rand_sequence)
        for count, n_gram in reversed(sorted(zip(markov_model._n_gram_counts.values(), markov_model._n_gram_counts.keys()))):
            if count > 1:
                print("{}/{}={} : {}".format(count,
                                             markov_model._count_sums[len(n_gram)],
                                             round(count/markov_model._count_sums[len(n_gram)], 3),
                                             n_gram))
        rand_sequence = [str(pitch) for pitch in rand_sequence]
        print(rand_sequence)
        n_measures = 2
        Loop(Sequence([
            Parallel([
                Measure(repack_list(rand_sequence, [2, 2, 2]), 4 * n_measures),
                Sequence([Measure(repack_list([Beat(sound='hh_c', amplitude=0.4)]*24, [3, 2, 2]), 4)] * n_measures),
                Sequence([Measure([[Beat(sound="kick"), Beat(sound="hh_c")],
                                   ["r", [Beat(sound="hh_c"), Beat(sound="ride")]],
                                   ["r", [Beat(sound="hh_c"), Beat(sound="snare", amplitude=4)]],
                                   ["r", [Beat(sound="hh_c"), Beat(sound="kick", amplitude=0.8)]]], 4)] * n_measures)
            ]),
            # Transposed(alle_mein_entchen, transpose=2, scale=scale),
            # m,
            ## quintuplets
            Parallel([
                # Measure(["c''", "r", "c''", "r", "c''", "r", "c''", "r", "c''", "r"], 4, 'b'),
                # Measure(['c', 'r', 'c', 'r', 'c', 'r', 'c', 'r'], 4, 'b'),
                # Measure(['b', 'r', 'b', 'r', 'b', 'r'], 4, 'b'),
            ]),
            # Loop(Sequence(
            #     [Beat(extent="1/4", amplitude=0.5),
            #      Chord(intervals=[0, 4], base="e", duration="1/4", amplitude=0.5),
            #      # Parallel([Tone("e", "1/4", amplitude=0.7), Tone("g#", "1/4", amplitude=0.7)]),
            #      # Event.parse_events("e/4 g#/4", agglomeration_type="Parallel"),
            #      Beat(extent="1/4", amplitude=1.),
            #      Rest("1/4")]
            # ), repeat=2),
            # # Loop(s, repeat=2),
            # Loop(Sequence(
            #     [Beat(extent="1/4", amplitude=0.5),
            #      Parallel([Tone("f#", "1/4", amplitude=0.5), Tone("a", "1/4", amplitude=0.5)]),
            #      Beat(extent="1/4", amplitude=1.),
            #      Rest("1/4")]
            # ), repeat=2)
        ]), "X").write(file)
        ##
        Event._indent -= 1
        print("end", file=file)
        print("", file=file)
        Event.write_loops(file)
        print("", file=file)
        Event.write_symbols(file)
        # write to sys out and real file
        print(file.getvalue())
        with open("song.rb", 'w') as song:
            print(file.getvalue(), file=song)

        # ## testing markov model
        # markov_model = MarkovModel(range(10))
        # markov_model.add_sequence([0, 1, 2, 3, 4])
        # markov_model.add_sequence([0, 1, 2, 3, 5])
        # markov_model.add_sequence([6])
        # markov_model.add_sequence([6])
        # markov_model.add_sequence([6])
        # print(markov_model._n_gram_counts)
        # print(markov_model._count_sums)
        # print(markov_model.get_distribution([0, 1, 2, 3]))

        # ## testing beam inference
        # model = TestModel(switch_time=5)
        # history = []
        # beam_inference = BeamInference(20, model)
        # print("probdist {}: {}".format(history, [model.probability(history, event) for event in model._alphabet]))
        # print(beam_inference.sample(6, history))
        # print(beam_inference._beams)
        # print(beam_inference._likelihoods)
