import mido
from mido import Message
import atexit

print("入力一覧：", mido.get_input_names())
print("出力一覧：", mido.get_output_names())

launchpad_in = 'Launchpad S 0'
launchpad_out = 'Launchpad S 1'

loopmidi_out = 'loopMIDI 2'  # LoopMIDIで作成したポート名

def reset_launchpad():
    for note in range(0, 128):
        mido.open_output(launchpad_out).send(Message('note_off', note=note, velocity=0))
    print("Launchpad has been reset (all LEDs off).")

atexit.register(reset_launchpad)

try:
    # Launchpadの入力ポートを開く
    with mido.open_output(loopmidi_out) as loopMIDI_outport, mido.open_input(launchpad_in) as inport:  # デバイス名をget_input_names()で確認
        print("Ready to receive messages. Press a button on the Launchpad.")
        
        # MIDIメッセージを待機し、受け取る
        for msg in inport:
            print(msg)  # MIDIメッセージの詳細を確認
            loopMIDI_outport.send(msg)

            # ノートオンメッセージのとき
            if msg.type == 'note_on' and msg.velocity > 0:
                print(f"Button {msg.note} pressed. Velocity: {msg.velocity}")
            
            # ノートオフメッセージ（ボタンを離したとき）
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                print(f"Button {msg.note} released.")

            # 特定のボタン（例: ノート番号 60）でループを終了
            if msg.type == 'note_on' and msg.note == 0:
                print("Exiting loop on button press.")
                break

except KeyboardInterrupt:
    print("Exiting...")



