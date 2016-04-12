import os
import json
import random
import requests
from django.http import JsonResponse
from django.views.generic import View


CHANNEL_ID = os.environ.get('CHANNEL_ID')
MID = os.environ.get('MID')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET', '')

ENDPOINT = 'https://trialbot-api.line.me/v1/events'
FIXIE_URL = os.environ.get('FIXIE_URL')  # for heroku


def text():
    msgs = [
        '1. 泣くな親父',
        '2. MEGA SHAKE IT !',
        '3. イマジネンス',
        '4. ビーフ or チキン',
        '5. NEKOSAMA',
        '6. フラッシュバック',
        '7. 春になっても',
        '8. 記憶にございません',
        '9. ハッピーポンコツ',
        '10. ヤブ医者',
        '11. 適度に武士道、サムライBOYS。',
    ]
    return {
        'contentType': 1,
        'toType': 1,
        'text': random.choice(msgs)
    }


def traverse(results):
    proxies = {'https': FIXIE_URL}
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': CHANNEL_ID,
        'X-Line-ChannelSecret': CHANNEL_SECRET,
        'X-Line-Trusted-User-With-ACL': MID
    }
    payload = {
        'toChannel': 1383378250,
        'eventType': '138311608800106203',
    }
    for result in results:
        payload.update({
            'to': [result['content']['from']],
            'content': text()
        })
        req = requests.post(ENDPOINT,
                            headers=headers,
                            data=json.dumps(payload),
                            proxies=proxies)
        print('request')
        print(req.__dict__)


class ArabakiView(View):
    http_method_names = ['get', 'post']

    def get(self, *args, **kwargs):
        return JsonResponse({
            'name': 'arabaki rock festival'
        })

    def post(self, request, *args, **kwargs):
        traverse(json.loads(request.body.decode())['result'])
        return JsonResponse({'status': 'ok'})
