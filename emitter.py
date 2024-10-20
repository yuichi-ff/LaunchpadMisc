import mido
from mido import Message
import atexit

print("入力一覧：", mido.get_input_names())
print("出力一覧：", mido.get_output_names())

launchpad_in = 'Launchpad S 0'
launchpad_out = 'Launchpad S 1'
loopmidi_out = 'loopMIDI 2'

def reset_launchpad():
    for note in range(0, 128):
        mido.open_output(launchpad_out).send(Message('note_off', note=note, velocity=0))
        mido.open_output(loopmidi_out).send(Message('note_off', note=note, velocity=0))
    for control_number in range(104, 112):
        mido.open_output(launchpad_out).send(Message('control_change', control=control_number, value=0))

atexit.register(reset_launchpad)

COLOR = 62
try:
    with    mido.open_input(launchpad_in) as inport, \
            mido.open_output(launchpad_out) as outport, \
            mido.open_output(loopmidi_out) as loopMIDI_outport:
        
        outport.send(Message('control_change', control=111, value=67))
        
        for msg in inport:
            print(msg)
            loopMIDI_outport.send(msg)

            if msg.type == 'note_on' and msg.velocity > 0:
                outport.send(Message('note_on', note=msg.note, velocity=COLOR))
                print("velocity",COLOR)
                print(f"Button {msg.note} pressed. Velocity: {msg.velocity}")
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                outport.send(Message('note_off', note=msg.note, velocity=0))
                print(f"Button {msg.note} released.")

            if msg.type == 'control_change' and msg.control == 111:
                break

except KeyboardInterrupt:
    print("Exiting...")



