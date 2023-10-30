import json

# JSONデータ（上記の例を使用）
json_data = '''
{
  "dialogue": [
    {
      "speakerID": 4,
      "message": "こんにちは、四国めたん！最近どうだった？"
    },
    {
      "speakerID": 3,
      "message": "ずんだもん！元気だよ。最近、香川の讃岐うどん食べたんだ。美味しかったなぁ。"
    },
    {
      "speakerID": 4,
      "message": "ほんと？いいなぁ。ぼくもまた食べに行きたいな。"
    },
    {
      "speakerID": 2,
      "message": "みんなこんにちは！きりたんぽもいますよ。"
    },
    {
      "speakerID": 2,
      "message": "ずんだもん、四国めたん、お二人とも元気そうで何よりです。"
    },
    {
      "speakerID": 4,
      "message": "きりたんぽも一緒にうどん食べない？"
    },
    {
      "speakerID": 3,
      "message": "いいね、大歓迎だよ！"
    },
    {
      "speakerID": 2,
      "message": "それでは、次のうどん会でお会いしましょう！"
    }
  ]
}
'''

# JSONデータを読み込む
data = json.loads(json_data)


for i, item in enumerate(data['dialogue']):
    comment = item['message']
    speaker_id = item['speakerID']
    print(speaker_id)