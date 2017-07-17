from unittest import TestCase
from MusicTreequence import *


def simplify_whitespace(string):
    return ' '.join(string.split())


class TestEvent(TestCase):

    def test_to_MIDI_pitch(self):
        self.assertEqual(60, Event.to_MIDI_pitch("c'"))
        self.assertEqual(60, Event.to_MIDI_pitch("c1"))
        self.assertEqual(60, Event.to_MIDI_pitch(60))
        self.assertEqual(60, Event.to_MIDI_pitch("60"))

    def test_to_beat_duration(self):
        Event.init()
        Event.beat_duration = 128
        self.assertEqual(128, Event.to_ms_duration("1"))
        self.assertEqual(64, Event.to_ms_duration("1/2"))
        self.assertEqual(32, Event.to_ms_duration(1 / 4))
        self.assertEqual(17, Event.to_ms_duration("17ms"))


class TestNoteEvent(TestCase):

    def test_generate(self):
        sequence_event = SequenceEvent([
            NoteEvent("c", "1/4"),
            RestEvent(1/4),
            NoteEvent("c0", 1 / 4),
            NoteEvent("c1", 0.25),
            NoteEvent("C1", "250ms")
        ])
        # tiny
        Event.init()
        sequence_event.generate()
        # print(Event.generation_output)
        self.assertEqual(simplify_whitespace(Event.generation_output), "c4 r4 c4 cc4 CC2")
        n = NoteEvent("c", 0.26)
        self.assertRaises(UserWarning, n.generate)
        # sonic
        Event.init()
        Event.generation_mode = GenMode.SONICPI
        sequence_event.sequence = [Event().set_beat("120bpm")] + sequence_event.sequence + [NoteEvent("C1", "251ms")]
        sequence_event.generate()
        # print(Event.generation_output)
        self.assertEqual(Event.generation_output, """# beat duration: 500.0ms/120.0bpm
play 48, attack: 0.01, decay: 0.125, sustain: 0.01, release: 0.01
sleep 0.125
sleep 0.125
play 48, attack: 0.01, decay: 0.125, sustain: 0.01, release: 0.01
sleep 0.125
play 60, attack: 0.01, decay: 0.125, sustain: 0.01, release: 0.01
sleep 0.125
play 24, attack: 0.01, decay: 0.25, sustain: 0.01, release: 0.01
sleep 0.25
play 24, attack: 0.01, decay: 0.251, sustain: 0.01, release: 0.01
sleep 0.251
""")
