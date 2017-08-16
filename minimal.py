import io
import random
import string

def to_MIDI_pitch(pitch):
    """map to midi pitch"""
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
    if isinstance(pitch, int):
        return pitch
    elif isinstance(pitch, str):
        try:
            pitch = int(pitch)
        except ValueError:
            return MIDI_pitch[pitch]
        return pitch

class Event(object):

    indent = 0
    beat = 1
    symbols = {}

    @staticmethod
    def write_indent(file):
        for _ in range(Event.indent):
            print("  ", end="", file=file)

    @staticmethod
    def get_extent(extent):
        if isinstance(extent, str):
            if extent.endswith("sec"):
                # sec
                return float(extent[:-3])
            elif extent.endswith("ms"):
                # ms --> sec
                return float(extent[:-2])/1000
            elif extent.endswith("b"):
                # beats --> sec
                return float(extent[:-1]) * Event.beat
            elif '/' in extent:
                # beat fraction x/y --> sec
                parts = extent.split('/')
                return float(parts[0]) / float(parts[1]) * Event.beat
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
                Event.beat = float(60000 / float(beat[:-3]))
            else:
                Event.beat = float(beat)
        else:
            Event.beat = beat

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
        for function_name, extent, function in Event.symbols.values():
            print(function, file=file)
            print("", file=file)

    def create_symbol(self, symbol):
        function_name = Event.random_string()
        with io.StringIO() as file:
            old_indent = Event.indent
            print("def {} # {}".format(function_name, symbol), file=file)
            Event.indent = 1
            self.write(file)
            print("end", end='', file=file)
            Event.indent = old_indent
            Event.symbols[symbol] = (function_name, self.extent(), file.getvalue())

    def extent(self):
        return 0

    def write(self, file):
        pass


class Tone(Event):

    def __init__(self, pitch, duration, extent=None, amplitude=1., symbol=None):
        self.pitch = pitch
        self.duration = duration
        self._extent = duration if extent is None else extent
        self.amplitude = amplitude
        if symbol is not None:
            self.create_symbol(symbol)

    def extent(self):
        return Event.get_extent(self._extent)

    def write(self, file):
        Event.write_indent(file)
        print("tone pitch: {}, duration: {}, amp: {}".format(to_MIDI_pitch(self.pitch),
                                                             Event.get_extent(self.duration),
                                                             self.amplitude),
              file=file)


class Beat(Event):

    def __init__(self, extent=0., amplitude=1., symbol=None):
        self._extent = extent
        self.amplitude = amplitude
        if symbol is not None:
            self.create_symbol(symbol)

    def extent(self):
        return Event.get_extent(self._extent)

    def write(self, file):
        Event.write_indent(file)
        print("play_beat amp: {}".format(self.amplitude), file=file)

class Break(Event):
    def __init__(self, extent, symbol=None):
        self._extent = extent
        if symbol is not None:
            self.create_symbol(symbol)

    def extent(self):
        return Event.get_extent(self._extent)

    def write(self, file):
        pass


class Sequence(Event):
    def __init__(self, sequence, symbol=None):
        self.sequence = sequence
        if symbol is not None:
            self.create_symbol(symbol)

    def extent(self):
        extent = 0
        for event in self.sequence:
            extent += event.extent()
        return extent

    def write(self, file):
        for event in self.sequence:
            event.write(file=file)
            if event.extent() > 0:
                Event.write_indent(file)
                print("sleep {}".format(event.extent()), file=file)


class Symbol(Event):

    def __init__(self, symbol):
        self.symbol = symbol

    def extent(self):
        return Event.symbols[self.symbol][1]

    def write(self, file):
        Event.write_indent(file)
        print("{} # {}".format(Event.symbols[self.symbol][0], self.symbol), file=file)

if __name__ == "__main__":
    with io.StringIO() as file:
        # create events and write to string-file
        Event.set_beat(1)
        print("def song", file=file)
        Event.indent += 1
        Sequence([
            Beat(extent="1/2", amplitude=0.5, symbol="A"),
            Tone("e", "1/2", extent="1/2", amplitude=0.7, symbol="B"),
            Beat(extent="1/2", amplitude=1., symbol="C"),
            Break("1/2"),
            Symbol("A"), Symbol("B"), Symbol("C")
        ]).write(file=file)
        Event.indent -= 1
        print("end", file=file)
        print("", file=file)
        Event.write_symbols(file)
        # write to sys out and real file
        print(file.getvalue())
        with open("song.rb", 'w') as song:
            print(file.getvalue(), file=song)