from music21 import *
import random
import logging

logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger(__name__+'.MusicTreequence').setLevel(logging.WARNING)
# logging.warning('Why do I need to print this to get logging output???')

class Event(object):

    logger = logging.getLogger()
    beat_length = 0  # in milliseconds
    time_signature = "4/4"
    # mode for generation
    #     "tinynotation": generate string that can be parsed by music21
    #     "SonicPi": generate Ruby code that can be interpreted by SonicPi
    generation_mode = "tinynotation"
    generation_output = ""
    generation_output_file = "out.txt"

    @staticmethod
    def reset(beat_length=True,
              time_signature=True,
              generation_mode=True,
              generation_output=True):
        if beat_length:
            Event.beat_length = 0
        if time_signature:
            Event.time_signature = "4/4"
        if generation_mode:
            Event.generation_mode = "tinynotation"
        if generation_output:
            Event.generation_output = ""


    @staticmethod
    def length(value, unit='ms'):
        """Compute event length from value.
        :param value: length of event.
        :param unit: unit for value. Either 'ms' for milliseconds (default) or 'beat' for beat.
        :return length in milliseconds"""
        if isinstance(value, int):
            return value
        else:
            return value * Event.beat_length

    @staticmethod
    def set_global_beat(value):
        """Set beat length.
        :param value: Either numeric in milliseconds or a string ending on 'bpm' with the
        remaining part giving the number of beats per minute."""
        if isinstance(value, int):
            Event.beat_length = value
        else:
            Event.beat_length = int(60000 / int(value.replace('bpm', '', 1)))

        logging.debug("set_global_beat() [{}]".format(Event.beat_length))

        if Event.generation_mode == "tinynotation":
            pass  # ignored
        elif Event.generation_mode == "SonicPi":
            Event.generation_output += "beatlength = {}\n".format(Event.beat_length)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))


    @staticmethod
    def set_global_time_signature(value):
        logging.debug("set_global_time_signature() [{}]".format(value))
        Event.time_signature = value
        if Event.generation_mode == "tinynotation":
            Event.generation_output += " " + value + " "
        elif Event.generation_mode == "SonicPi":
            Event.generation_output += "# time signature: {}\n".format(value)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    def __init__(self):
        # self.generate_prefix = ""
        # self.generate_content = ""
        # self.generate_postfix = ""
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
        if Event.generation_mode == "tinynotation":
            return
        elif Event.generation_mode == "SonicPi":
            return
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    def show(self, mode="tinynotation"):
        Event.generation_mode = mode
        self.generate()
        print(Event.generation_output)
        if Event.generation_mode == "tinynotation":
            return converter.parse("tinynotation: " + Event.generation_output).show()
        elif Event.generation_mode == "SonicPi":
            with open(Event.generation_output_file, 'w') as file:
                file.write(Event.generation_output)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

    # def one_of_params(self, param_list):
    #     for param in param_list:
    #         if param is not None:
    #             return True
    #     raise UserWarning("All parameters are 'None'")


class NoteEvent(Event):

    def __init__(self, pitch, length):
        Event.__init__(self)
        self.pitch = pitch
        self.length = length

    def generate(self):
        logging.debug("NoteEvent.generate() [{}, {}]".format(self.pitch, self.length))
        """Generate representation of event"""
        self.performe_scheduled_operations()
        if Event.generation_mode == "tinynotation":
            Event.generation_output += " " + str(self.pitch) + str(self.length) + " "
        elif Event.generation_mode == "SonicPi":
            Event.generation_output += "play {}\n".format(self.pitch)
            Event.generation_output += "sleep {}\n".format(self.length)
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
            Event.generation_output += " "
            e.generate()
        Event.generation_output += " "


class RandomEvent(Event):
    def generate(self):
        logging.debug("RandomEvent.generate()")
        if Event.generation_mode == "tinynotation":
            Event.generation_output += " " + random.choice(["c4", "d8", "f", "g16", "a", "g", "f#", "c4", "d8", "f", "g16", "a", "g", "f#"]) + " "
        elif Event.generation_mode == "SonicPi":
            Event.generation_output += "play {}".format(random.randint(60, 84))
            Event.generation_output += "sleep {}".format(random.choice([2, 1, 1/2])*Event.beat_length)
        else:
            raise UserWarning("Unknown mode '{}'".format(Event.generation_mode))

class MeasureEvent(Event):

    def __init__(self, beats=None, length=None, time_signature=None):
        super(MeasureEvent, self).__init__()
        Event.__init__(self)
        # self.one_of_params([beats, length, time_signature])


# if __name__ == '__main__':
#     main()