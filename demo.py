
from MusicTreequence import *

minor = (0, 3, 7)
major = (0, 4, 7)
minor7 = (0, 3, 7, 10)
major7 = (0, 4, 7, 11)
dom7 = (0, 4, 7, 10)
half_dim = (0, 3, 6, 10)
dim = (0, 3, 6, 9)
aug = (0, 4, 8)

kick = Beat(sound="kick")
snare = Beat(sound="snare")
hh_c = Beat(sound="hh_c")
hh_o = Beat(sound="hh_o")
ride = Beat(sound="ride")
rest = Rest()

base = to_MIDI_pitch("c")
amp = 0.2

# scale = TonicScale(pitches=["c", "d", "e", "f", "g", "a", "b"])
scale = TonicScale(pitches=["c", "d", "eb", "f", "g", "ab", "bb"])
scale._tonic = base
bass_line = [pitch for pitch in range(base, base + 13) if scale.is_in_scale(pitch)]


def arpeggiate(chord, base, n, extent, *args, **kwargs):
    seq = [str(base + chord[i % len(chord)]) for i in range(n)]
    return Measure([Tone(pitch, staccato=True, *args, **kwargs) for pitch in seq], extent=extent)


with write_song('song.rb', print_to_std_out=True):
    Event.set_beat("120bpm")
    Loop(
        Parallel([
            arpeggiate(rotate(minor7, 8), base, 32, 8, amplitude=0.5),
            arpeggiate(minor7, base, 16, 8),
            arpeggiate(rotate(minor, 3), base, 16, 8),
            Sequence([Tone(to_MIDI_pitch(pitch)-12, staccato=True, synth=":saw") for pitch in bass_line]),
            # Measure([
            #             [kick],
            #             [snare, hh_c],
            #             [kick, hh_c],
            #             [snare, hh_c],
            #         ] * 2, extent=8),
            # Measure([
            #             [hh_c] * 3,
            #             [rest],
            #             [rest, rest, rest, ride],
            #             [rest],
            #         ] * 2, extent=8),
            Measure([
                [kick],
                [hh_c, [hh_c] * 2],
                [snare, hh_c],
                [rest, ride]
            ] * 2, extent=8),
            # Measure([
            #     [rest],
            #     [rest],
            #     [rest],
            #     [rest, kick]
            # ] * 2, extent=8),
            # Measure([
            #     [[[hh_c, rest, hh_c]] * 2],
            #     [[hh_c, rest, hh_c] * 2],
            # ] * 2, extent=8)
        ]),
        symbol="main_loop"
    ).write()