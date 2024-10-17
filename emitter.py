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

atexit.register(reset_launchpad)

color = 0
try:
    with    mido.open_input(launchpad_in) as inport, \
            mido.open_output(launchpad_out) as outport, \
            mido.open_output(loopmidi_out) as loopMIDI_outport:
        
        for msg in inport:
            print(msg)
            loopMIDI_outport.send(msg)

            if msg.type == 'note_on' and msg.velocity > 0:
                color+=1
                outport.send(Message('note_on', note=msg.note, velocity=color))
                print("velocity",color)
                print(f"Button {msg.note} pressed. Velocity: {msg.velocity}")
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                outport.send(Message('note_off', note=msg.note, velocity=0))
                print(f"Button {msg.note} released.")

            if msg.type == 'note_on' and msg.note == 0:
                break

except KeyboardInterrupt:
    print("Exiting...")



