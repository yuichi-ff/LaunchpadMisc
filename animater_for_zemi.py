import mido
from mido import Message
import atexit
import time

print("入力一覧：", mido.get_input_names())
print("出力一覧：", mido.get_output_names())

frames = [
    [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,1,0,0,1,0,1],
    [1,0,0,1,1,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0],
    ],
    [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,1,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,0,1,0,0,1],
    [1,0,1,1,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0],
    ],
    [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,1,0,0,0,1],
    [1,0,1,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0],
    ],
    [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0],
    ],
        [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0],
    ],
    ]

launchpad_in = 'Launchpad S 0'
launchpad_out = 'Launchpad S 1'

loopmidi_out = 'loopMIDI 2'  # LoopMIDIで作成したポート名

def reset_launchpad():
    for note in range(0, 128):
        mido.open_output(launchpad_out).send(Message('note_off', note=note, velocity=0))
    print("Launchpad has been reset (all LEDs off).")

atexit.register(reset_launchpad)

try:
    with    mido.open_input(launchpad_in) as inport, \
            mido.open_output(launchpad_out) as outport, \
            mido.open_output(loopmidi_out) as loopMIDI_outport:
        
        for i in range(5):
            for frame in frames:
                time.sleep(0.2)
                for i in range(8):
                    for j in range(8):
                        noteid = i * 16 + j
                        outport.send(Message('note_on', note=noteid, velocity=frame[i][j] * 61))

            for i in range(len(frames)-1,0,-1):
                frame = frames[i]
                time.sleep(0.2)
                flipped_frames = [list(reversed(row)) for row in frame]
                for i in range(8):
                    for j in range(8):
                        noteid = i * 16 + j
                        outport.send(Message('note_on', note=noteid, velocity=flipped_frames[i][j] * 61))

except KeyboardInterrupt:
    print("Exiting...")



