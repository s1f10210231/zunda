import os

# 動画ファイルが入っているフォルダのパス
folder_path = "./onnxruntime-linux-x64-1.13.1/shortgenerate"


# フォルダ内の動画ファイルのパスを取得
video_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.mp4', '.avi', '.mkv'))]

# ファイルの順番を降順にソート
video_paths.sort(reverse=False)

# テキストファイルに動画パスを書き込む
with open('list.txt', 'w') as file:
    for path in video_paths:
        file.write(f'file {path}\n')

print('動画ファイルのパスを降順に list.txt に書き込みました。')
