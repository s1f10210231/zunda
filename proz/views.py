from django.shortcuts import render, redirect
import openai
import proz.zunmovie.movie as zm
openai.api_key="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"


def zunda_create(text):
  response = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[
          {'role':'user','content':
          f'''#命令書:
  あなたはプロのYouTube作家です。
  以下の制約条件と入力文をもとに、30段落程度で詳細や具体例にも触れた最高の会話を出力してください。

  #制約条件:
  ・ずんだもんと四国めたんという二人のキャラクターが会話しているように書く。
  ・二人の一人称は「私」。
  ・二人は互いににタメ口で会話する。
  ・四国めたんは知識豊富な解説役。
  ・四国めたんは少し気の強い女性。
  ・四国めたんは語尾に「～ぜ」「～だぜ」「～だよな」「～だ」「～だな」を使うことが非常に多い。
  ・ずんだもんは少し知識に疎く、四国めたんに対する質問役。
  ・ずんだもんは穏やかな話し方をする女性。
  ・ずんだもんは語尾に「～なのだ」「～のだ」「～だ」を使うことが非常に多い。
  ・ずんだもんは四国めたんの解説についてよく聞き、自然な会話で内容について質問をする。
  ・会話は以下のパターンを一段落とし、繰り返す
  四国めたんの解説→ずんだもんの感想→四国めたんの追加解説→ずんだもんから質問→四国めたんの回答
  ・会話は次の文章から開始すること。
  [今日は{text}について解説するぜ,よろしくお願いするのだ！]
  ・会話の最後は、以下の文章で終わること
  [今日はここまでだぜ,ご視聴ありがとうなのだー]

  """
  {text}

  """


  '''},
          {'role':'user','content':"""
            #制約条件
          ・話者の名前は
          {ずんだもん:3},{四国めたん:4}とspeakerIDを設定してください。
          ・{キャラクター}の名前はいれずにセリフだけを格納してください。
          #命令文
          今、出力した二人のセリフだけ（話者の名前はいれない）をJSONフォーマットに変換してください。リストに格納する順番は生成された通りで、
          例えば、
          {キャラクター}「今日は坂本龍一について解説するぜ」
          {キャラクター}「よろしくお願いするのだ！」
          というものがあれば
           
  {"dialogue": [
      {
        "speakerID": 4,
        "message": "ずんだもん、こんにちは！最近の天気、知ってる？"
      },
      {
        "speakerID": 3,
        "message": "四国めたん、こんにちは！うーん、今日はどうだろう？"
      }
          ...と続いてください。
          
          /
          ・制約条件を必ず守り命令文を実行してください。
        

          """},
          {"role":"assistant","content":"{"},


      ]
  )
  print(response['choices'][0]['message']['content'])
  return response['choices'][0]['message']['content']

def index(request):
    video_path = "/media/movie/complete.mp4"
    if(request.method=="POST"):
        texts = request.POST.get('zunda_input', '')
        text= "{" + zunda_create(texts)
        zm.zunda_movie(text)
    context = {
       'video_url':video_path,
    }
    return render(request,"proz/index.html",context)