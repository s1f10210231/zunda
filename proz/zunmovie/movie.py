from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import textwrap  # 追加：textwrapモジュールをインポート
# Function to add text and replace the circle with an image, handling text overflow
import numpy as np
from pathlib import Path
import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore
from playsound import playsound
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.editor import *
import subprocess
import glob
import math
import json
count=0
def zunda_movie(text_zun):
    def format_index(i):
        # iが100以上の場合は4桁のゼロ埋め、それ以外の場合は1～3桁のゼロ埋め
        return f"{i:04d}" if i >= 100 else f"{i:03d}"

    import os
    import shutil

    def delete_folder_contents(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    # 動画生成のために作成されたフォルダのパス
    folders_to_clear = [
        "./zunmovie/moviebox",
        "./zunmovie/shortgenerate",
        "./zunmovie/generate",
        "./v_output"
    ]

    # 各フォルダの中身を削除
    for folder_path in folders_to_clear:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            delete_folder_contents(folder_path)

    print("フォルダの中身は削除されました。")


    path = os.path.abspath("./proz/list.txt")
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    print("不要なファイルおよびフォルダは削除されました。")




    open_jtalk_dict_dir = os.path.abspath('./proz/open_jtalk_dic_utf_8-1.11')
    acceleration_mode = AccelerationMode.AUTO


    def alpha_blend(frame, alpha_frame, position):
        if frame is not None and alpha_frame is not None:
            x1, y1 = max(position[0], 0), max(position[1], 0)
            x2 = min(position[0] + alpha_frame.shape[1], frame.shape[1])
            y2 = min(position[1] + alpha_frame.shape[0], frame.shape[0])
            ax1, ay1 = x1 - position[0], y1 - position[1]
            ax2, ay2 = ax1 + x2 - x1, ay1 + y2 - y1

            frame[y1:y2, x1:x2] = frame[y1:y2, x1:x2] * (1 - alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255) + \
                                alpha_frame[ay1:ay2, ax1:ax2, :3] * (alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255)

    def putText_japanese(img, text, pos, size, color,outline_color,width):
        font_path = os.path.abspath("./proz/zunmovie/font/ipaexg.ttf")
        font = ImageFont.truetype(font_path, size)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        # テキスト描画（縁取りあり）
        draw.multiline_text(pos, text, fill=color, font=font,stroke_fill=outline_color,stroke_width=width)

        return np.array(img_pil)

    def generate_comment_video(comment, output_path,speaker_id):
        font_path = os.path.abspath("./proz/zunmovie/font/ipaexg.ttf")

        pos_x,pos_y = (10, 10)  # Text position
        font_size = 50
        bgr = (0, 0, 0)  # Text color (black)
        outline_color=(255,255,255)
        width=3
        img = np.ones((720, 1280, 3), np.uint8) * 255  # White background

        image_path1 = os.path.abspath("./proz/zunmovie/image/ずんだもん立ち絵素材2_0000.png")
        image_path2 = os.path.abspath("./proz/zunmovie/image/四国めたん立ち絵素材2_0000.png")
        image_path3 = os.path.abspath("./proz/zunmovie/image/天気予報.png")

        png_image = cv2.imread(image_path1, cv2.IMREAD_UNCHANGED)
        alpha_blend(img, png_image, (920, 200))

        png_image = cv2.imread(image_path2, cv2.IMREAD_UNCHANGED)
        alpha_blend(img, png_image, (-10, 200))


        png_image = cv2.imread(image_path3, cv2.IMREAD_UNCHANGED)   
        alpha_blend(img, png_image, (315, 100))

        img = putText_japanese(img, "ずんだもんの嘘っぱちニュースをやってみた", (pos_x,pos_y), font_size, bgr,outline_color,width)
        font_size = 35

        annotated_image = img.copy()
        cv2.rectangle(img, (0, 580), (1280, 800), (60, 60, 60), thickness=-1)
        img = cv2.addWeighted(annotated_image, 0.2, img, 0.8, 0)

        outline_color=(255,255,255)

        if len(comment) > 27:
            msg_tl = comment[:27]
            comment2 = comment[27:]

            (x,y) = (180, 590)  # Text position for the first part
            if (speaker_id ==3):
                img = putText_japanese(img, msg_tl, (x,y), font_size, (4,203,90),outline_color,width)
            elif (speaker_id==4):
                img = putText_japanese(img, msg_tl, (x,y), font_size, (182,83,200),outline_color,width)

            else:
                img = putText_japanese(img, msg_tl, (x,y), font_size, (240, 230, 230),outline_color,width)

            
            print(msg_tl)

            if len(comment2) > 27:
                comment3 = comment2[:27]
                comment4 = comment2[27:]

                (x,y) = (180, 637)  # Text position for the second part (first part of comment2)
            
                if (speaker_id ==3):
                    img = putText_japanese(img, comment3, (x,y), font_size, (4,203,90),outline_color,width)
                elif (speaker_id==4):
                    img = putText_japanese(img, comment3, (x,y), font_size, (182,83,200),outline_color,width)
                else:
                    img = putText_japanese(img, comment3, (x,y), font_size, (240, 230, 230),outline_color,width)
                (x,y) = (180, 680)  # Text position for the third part (second part of comment2)
                if (speaker_id ==3):
                    img = putText_japanese(img, comment4, (x,y), font_size, (4,203,90),outline_color,width)
                elif (speaker_id==4):
                    img = putText_japanese(img, comment4, (x,y), font_size, (182,83,200),outline_color,width)
                else:
                    img = putText_japanese(img, comment4, (x,y), font_size, (240, 230, 230),outline_color,width)
            else:
                (x,y) = (180, 640)  # Text position for the second part (comment2 is within 27 characters)
                if (speaker_id ==3):
                    img = putText_japanese(img, comment2, (x,y), font_size, (4,203,90),outline_color,width)
                elif (speaker_id==4):
                    img = putText_japanese(img, comment2, (x,y), font_size, (182,83,200),outline_color,width)
                else:
                    img = putText_japanese(img, comment2, (x,y), font_size, (240, 230, 230),outline_color,width)

        else:
            (x,y) = (180, 590)  # Text position for the second part (comment2 is within 27 characters)
            if (speaker_id ==3):
                img = putText_japanese(img, comment, (x,y), font_size, (4,203,90),outline_color,width)
            elif (speaker_id==4):
                img = putText_japanese(img, comment, (x,y), font_size, (182,83,200),outline_color,width)
            else:
                img = putText_japanese(img, comment, (x,y), font_size, (240, 230, 230),outline_color,width)

        video_filename = output_path
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
        video = cv2.VideoWriter(video_filename, fourcc, 0.1, (1280, 720))

        for _ in range(len(comment)):  # Repeat the frame for 5 seconds
            video.write(img)

        video.release()  # Close the video file

    json_data = f'''{text_zun}'''

    data = json.loads(json_data)
    msglist=[]

    SpeakerID=[]


    for i, item in enumerate(data['dialogue']):
        comment = item['message']
        speaker_id = item['speakerID']
        msglist.append(comment)
        SpeakerID.append(speaker_id)
        
        output_path = f"./proz/zunmovie/moviebox/comment_{format_index(i)}.mp4"
        generate_comment_video(comment, output_path,speaker_id)
        print(f"動画 {i}: {output_path}")

    def get_audio_duration(audio_file_path):
        # 音声ファイルを読み込む
        audio_clip = AudioFileClip(audio_file_path)

        # 音声ファイルの長さ（秒単位）を取得
        duration_in_seconds = audio_clip.duration
        duration_in_milliseconds = int(duration_in_seconds * 1000)  # 秒をミリ秒に変換

        return duration_in_milliseconds

    # 使用例



    def synthesis(SPEAKER,txt):
        global count
        out = Path(f'./proz/v_output/output{format_index(count)}.wav')
        core = VoicevoxCore(
            acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
        )
        core.load_model(SPEAKER)
        audio_query = core.audio_query(txt, SPEAKER)
        wav=core.synthesis(audio_query, SPEAKER)
        out.write_bytes(wav)
        count+=1


        # エラーハンドリングを追加

    def join_text(text,speak):
    
        for i in range(len(text)):
            synthesis(speak[i], text[i])

    join_text(msglist,SpeakerID)
    print("音声合成完了")


    import math

    ## 動画を開始ミリ秒～終了ミリ秒までカットする
    ## 
    def trimVideo(targetFileName, destFileName, startMillis, stopMillis):
        ## FPS、フレーム数・開始終了フレーム番号取得
        videoCapture = cv2.VideoCapture(targetFileName)
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        totalFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        startFrameIndex = math.ceil(fps * startMillis / 1000)
        stopFrameIndex = math.ceil(fps * stopMillis / 1000)
        if(startFrameIndex < 0): 
            startFrameIndex = 0
        if(stopFrameIndex >= totalFrames):
            stopFrameIndex = totalFrames-1
        videoCapture.set(cv2.CAP_PROP_POS_FRAMES, startFrameIndex)
        frameIndex = startFrameIndex
        
        ## 開始～終了地点までフレーム分割
        imgArr = []
        while(frameIndex <= stopFrameIndex):
            _,img = videoCapture.read()
            imgArr.append(img)
            frameIndex += 1
            
        ## 分割フレームをmp4動画に再構成
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        video = None
        tmpVideoFileName = destFileName
        for img in imgArr:
            if(video is None):
                h,w,_ = img.shape
                video = cv2.VideoWriter(tmpVideoFileName, fourcc, 20.0, (w,h))
            video.write(img)
        if video is not None:  # Ensure video is created before release
            video.release()



    def merge_audio_video(audio_file, video_file, output_file,dist):
        # 音声ファイルを読み込む
        audio_clip = AudioFileClip(audio_file)

        # 無音の動画ファイルを読み込む
        
        trimVideo(video_file,dist,0,get_audio_duration(audio_file))  
        video_clip = VideoFileClip(dist)

        # 動画に音声を追加
        video_clip = video_clip.set_audio(audio_clip)

        # 結合した動画を保存
        video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)



    for i, comment in enumerate(msglist):
        audio_file = os.path.abspath(f"./proz/v_output/output{format_index(i)}.wav")
        video_file = os.path.abspath(f"./proz/zunmovie/moviebox/comment_{format_index(i)}.mp4")
        
        output_file = os.path.abspath(f"./proz/zunmovie/generate/outputvideo{format_index(i)}.mp4")
        dist = os.path.abspath(f"./proz/zunmovie/shortgenerate/outputvideo{format_index(i)}.mp4")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        os.makedirs(os.path.dirname(dist), exist_ok=True)
        merge_audio_video(audio_file, video_file, output_file,dist)



    folder_path = os.path.abspath("./proz/zunmovie/generate")

    # フォルダ内の動画ファイルのパスを取得
    video_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.mp4'))]

    # ファイルの順番を降順にソート
    video_paths.sort(reverse=False)

    # テキストファイルに動画パスを書き込む
    with open('./proz/list.txt', 'w') as file:
        for path in video_paths:
            file.write(f'file {path}\n')

    output = "media/movie/complete.mp4" # 出力ファイルのパスを修正
    list = os.path.abspath("./proz/list.txt")
    output2 = subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", list, output], input='y\n', text=True)



    import os
    import shutil

    def delete_folder_contents(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    # 動画生成のために作成されたフォルダのパス
    folders_to_clear = [
        "./proz/zunmovie/moviebox",
        "./proz/zunmovie/shortgenerate",
        "./proz/zunmovie/generate",
        "./proz/v_output"
    ]

    # 各フォルダの中身を削除
    for folder_path in folders_to_clear:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            delete_folder_contents(folder_path)

    print("フォルダの中身は削除されました。")


    # path = "./list.txt"
    # if os.path.exists(path):
    #     if os.path.isdir(path):
    #         shutil.rmtree(path)
    #     else:
    #         os.remove(path)

    print("不要なファイルおよびフォルダは削除されました。")