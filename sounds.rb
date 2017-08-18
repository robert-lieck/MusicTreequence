# Define sounds and other usefull stuff.

def tone(pitch:, duration:, amp:)
  play pitch, attack: 0.01, decay: duration, sustain: 0.1, release: 0.1, amp: amp
end

def play_beat(smp: :tabla_ghe1, amp: 1)
  ##| :drum_cymbal_closed :drum_snare_soft :tabla_ghe1
  sample smp, amp: amp
end
