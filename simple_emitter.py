import mido
from mido import Message

# Launchpad に接続する
output = mido.open_output('Launchpad S 1')  # デバイス名はシステムによって異なるので確認してください

# ボタン 0 を赤く点灯させる
msg = Message('note_on', note=0, velocity=3)  # ノート番号 0、ベロシティ 3 (赤)
output.send(msg)
