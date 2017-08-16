from music21 import *
from enum import Enum
import random
import logging
import numbers
import math
import minimal

logging.getLogger().setLevel(logging.INFO)
# logging.getLogger(__name__+'.MusicTreequence').setLevel(logging.WARNING)
# logging.warning('Why do I need to print this to get logging output???')


class GenMode(Enum):
    """mode for generation"""
    TINY = 0      # generate string that can be parsed by music21
    SONICPI = 1   # generate Ruby code that can be interpreted by SonicPi


class Event(object):

    logger = logging.getLogger()
    beat_duration = None  # in milliseconds
    time_signature = None
    generation_mode = None
    generation_output = None
    generation_output_file = None

    @staticmethod
    def init(beat_duration=True,
             time_signature=True,
             generation_mode=True,
             generation_output=True,
             generation_output_file=True):
        if beat_duration:
            Event.beat_duration = 500
        if time_signature:
            Event.time_signature = "4/4"
        if generation_mode:
            Event.generation_mode = GenMode.TINY
        if generation_output:
            Event.generation_output = ""
        if generation_output_file:
            Event.generation_output_file = "out.txt"


    @staticmethod
    def duration(value, unit='ms'):
        """Compute event duration from value.
        :param value: duration of event.
        :param unit: unit for value. Either 'ms' for milliseconds (default) or 'beat' for beat.
        :return duration in milliseconds"""
        if isinstance(value, int):
            return value
        else:
            return value * Event.beat_duration

    @staticmethod
    def set_global_beat(value):
        """Set beat duration"""
        logging.debug("set_global_beat() [{}]".format(value))
        if isinstance(value, str):
            if value.endswith('bpm'):
                value = float(60000 / float(value[:-3]))
            elif value.endswith('ms'):
                value = int(value[:-2])
        Event.beat_duration = value
        if Event.generation_mode == GenMode.TINY:
            pass
        elif Event.generation_mode == GenMode.SONICPI:
            Event.generation_output += "# beat duration: {}ms/{}bpm\n".format(value, 60000 / value)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    @staticmethod
    def set_global_time_signature(value):
        logging.debug("set_global_time_signature() [{}]".format(value))
        Event.time_signature = value
        if Event.generation_mode == GenMode.TINY:
            Event.generation_output += " " + value + " "
        elif Event.generation_mode == GenMode.SONICPI:
            Event.generation_output += "# time signature: {}\n".format(value)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    @staticmethod
    def to_MIDI_pitch(pitch):
        """map to midi pitch"""
        return minimal.to_MIDI_pitch(pitch)


    @staticmethod
    def to_tinynotation(pitch, duration):
        """generate representation for tinynotation"""
        if pitch is not None:
            if Event.to_MIDI_pitch(pitch) < 24:
                raise UserWarning("MIDI pitch {} to low for 'tinynotation'".format(pitch))
            if Event.to_MIDI_pitch(pitch) > 71:
                raise UserWarning("MIDI pitch {} to high for 'tinynotation'".format(pitch))
        pitch_name = {
            None: "r", # rest
            24: "CC", 25: "CC#", 26: "DD", 27: "DD#", 28: "EE", 29: "FF", 30: "FF#", 31: "GG", 32: "GG#", 33: "AA",
            34: "AA#", 35: "BB", 36: "C", 37: "C#", 38: "D", 39: "D#", 40: "E", 41: "F", 42: "F#", 43: "G", 44: "G#",
            45: "A", 46: "A#", 47: "B", 48: "c", 49: "c#", 50: "d", 51: "d#", 52: "e", 53: "f", 54: "f#", 55: "g",
            56: "g#", 57: "a", 58: "a#", 59: "b", 60: "cc", 61: "cc#", 62: "d'", 63: "dd#", 64: "ee", 65: "ff",
            66: "ff#", 67: "gg", 68: "gg#", 69: "aa", 70: "aa#", 71: "bb"
        }
        duration_name = {
            1: "1", 1 / 2: "2", 1 / 4: "4", 1 / 8: "8", 1 / 16: "16", 1 / 32: "32", 1 / 64: "64",
            1 / 128: "1/128"
        }
        return pitch_name[Event.to_MIDI_pitch(pitch)] + duration_name[
            Event.to_beat_duration(Event.to_ms_duration(duration))]

    @staticmethod
    def to_ms_duration(duration):
        """convert to duration in milliseconds"""
        if isinstance(duration, str):
            if duration.endswith("ms"):
                duration = float(duration[:-2])
            else:
                parts = duration.split('/')
                duration = float(parts[0])
                if len(parts) > 1:
                    duration /= float(parts[1])
                duration *= Event.beat_duration
        elif isinstance(duration, numbers.Number):
            duration *= Event.beat_duration
        return duration

    @staticmethod
    def to_sec_duration(duration):
        """convert to duration in seconds"""
        return Event.to_ms_duration(duration) / 1000

    @staticmethod
    def to_beat_duration(ms_duration):
        """convert millisecond duration into fractions of beat duration"""
        duration = ms_duration / Event.beat_duration
        for frac in [1, 1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64, 1 / 128]:
            if math.isclose(duration, frac):
                return frac
        raise UserWarning(
            "Duration of {} milliseconds ({} beats) is not a power-of-two fraction of beat duration ({})".format(
                ms_duration, duration, Event.beat_duration))

    def __init__(self):
        self.scheduled_operations = {}

    def set_beat(self, value):
        self.scheduled_operations['set_beat'] = value
        return self

    def set_time_signature(self, value):
        self.scheduled_operations['set_time_signature'] = value
        return self

    def performe_scheduled_operations(self):
        for key, value in self.scheduled_operations.items():
            if key == 'set_beat':
                Event.set_global_beat(value)
            elif key == 'set_time_signature':
                Event.set_global_time_signature(value)
            else:
                raise UserWarning("Unknown operation '{}' with value '{}' scheduled".format(key, value))

    def generate(self):
        logging.debug("Event.generate()")
        """Generate representation of event"""
        self.performe_scheduled_operations()
        if Event.generation_mode == GenMode.TINY:
            return
        elif Event.generation_mode == GenMode.SONICPI:
            return
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    def show(self, mode=GenMode.TINY):
        Event.generation_mode = mode
        self.generate()
        print(Event.generation_output)
        if Event.generation_mode == GenMode.TINY:
            return converter.parse("tinynotation: " + Event.generation_output).show()
        elif Event.generation_mode == GenMode.SONICPI:
            with open(Event.generation_output_file, 'w') as file:
                file.write("use_synth :fm\nuse_bpm 60\n")
                file.write(Event.generation_output)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    # def one_of_params(self, param_list):
    #     for param in param_list:
    #         if param is not None:
    #             return True
    #     raise UserWarning("All parameters are 'None'")


class NoteEvent(Event):

    def __init__(self, pitch, duration, forward=True):
        Event.__init__(self)
        self.pitch = pitch
        self.duration = duration
        self.forward = forward

    def generate(self):
        """Generate representation of event"""
        logging.debug("NoteEvent.generate() [{}, {}]".format(self.pitch, self.duration))
        self.performe_scheduled_operations()
        if Event.generation_mode == GenMode.TINY:
            Event.generation_output += " " + Event.to_tinynotation(self.pitch, self.duration) + " "
        elif Event.generation_mode == GenMode.SONICPI:
            Event.generation_output += "play {}, attack: 0.01, decay: {}, sustain: 0.01, release: 0.01\n".format(
                Event.to_MIDI_pitch(self.pitch), Event.to_sec_duration(self.duration))
            if self.forward:
                Event.generation_output += "sleep {}\n".format(Event.to_sec_duration(self.duration))
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))


class RestEvent(Event):

    def __init__(self, duration):
        Event.__init__(self)
        self.duration = duration

    def generate(self):
        """Generate representation of event"""
        logging.debug("RestEvent.generate() [{}]".format(self.duration))
        self.performe_scheduled_operations()
        if Event.generation_mode == GenMode.TINY:
            Event.generation_output += " " + Event.to_tinynotation(None, self.duration) + " "
        elif Event.generation_mode == GenMode.SONICPI:
                Event.generation_output += "sleep {}\n".format(Event.to_sec_duration(self.duration))
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))


class SequenceEvent(Event):

    def __init__(self, sequence):
        Event.__init__(self)
        self.sequence = sequence

    def generate(self):
        logging.debug("SequenceEvent.generate()")
        Event.performe_scheduled_operations(self)
        for e in self.sequence:
            e.generate()


class RandomEvent(Event):
    def generate(self):
        logging.debug("RandomEvent.generate()")
        if Event.generation_mode == GenMode.TINY:
            Event.generation_output += " " + random.choice(["c4", "d8", "f", "g16", "a", "g", "f#", "c4", "d8", "f", "g16", "a", "g", "f#"]) + " "
        elif Event.generation_mode == GenMode.SONICPI:
            Event.generation_output += "play {}".format(random.randint(60, 84))
            Event.generation_output += "sleep {}".format(random.choice([2, 1, 1/2])*Event.beat_duration)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

class MeasureEvent(Event):

    def __init__(self, beats=None, duration=None, time_signature=None):
        super(MeasureEvent, self).__init__()
        Event.__init__(self)
        # self.one_of_params([beats, duration, time_signature])


# if __name__ == '__main__':
#     main()