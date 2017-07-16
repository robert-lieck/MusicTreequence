from MusicTreequence import *

Event.reset()
SequenceEvent([
    NoteEvent("c", "4").set_time_signature("3/4"),
    NoteEvent("c#", "4").set_beat("100bpm"),
    NoteEvent("d", "4"),
    NoteEvent("d#", "4").set_time_signature("4/4"),
    NoteEvent("e", "4"),
    NoteEvent("f", "4"),
    NoteEvent("g", "4"),
    NoteEvent("g#", "4"),
    NoteEvent("a", "4"),
    NoteEvent("a#", "4"),
    NoteEvent("b", "4"),
    NoteEvent("c", "4"),
]).show()