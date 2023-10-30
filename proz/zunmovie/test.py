from pathlib import Path
import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore
from playsound import playsound


open_jtalk_dict_dir = './open_jtalk_dic_utf_8-1.11'
text = ['次のオリンピックはパリで行われるのだ。','今回のオリンピックには新競技もあって、全世界が注目しているんだってさ。。。','意義ありなのだ']
SpeakerID=[3,4]
acceleration_mode = AccelerationMode.AUTO
count=0
def synthesis(SPEAKER,txt):
    global count
    out = Path(f'output{count}.wav')
    core = VoicevoxCore(
        acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
    )
    core.load_model(SPEAKER)
    audio_query = core.audio_query(txt, SPEAKER)
    wav=core.synthesis(audio_query, SPEAKER)
    out.write_bytes(wav)
    count+=1


    # エラーハンドリングを追加

import wave

def join_waves(inputs, output):
    '''
    inputs : list of filenames
    output : output filename
    '''
    try:
        fps = [wave.open(f, 'r') for f in inputs]
        fpw = wave.open(output, 'w')

        fpw.setnchannels(fps[0].getnchannels())
        fpw.setsampwidth(fps[0].getsampwidth())
        fpw.setframerate(fps[0].getframerate())
        
        for fp in fps:
            fpw.writeframes(fp.readframes(fp.getnframes()))
            fp.close()
        fpw.close()

    except wave.Error as e:
        print(e)

    except Exception as e:
        print('unexpected error -> ' + str(e))


inputs = ['output'+str(n) + '.wav' for n in range(len(text))]
output = '99.wav'

def join_text():
    for i in range(len(text)):
        speaker_index = i % len(SpeakerID)
        synthesis(SpeakerID[speaker_index], text[i])

join_text()
print("音声合成完了")
join_waves(inputs, output)