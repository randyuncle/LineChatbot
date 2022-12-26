import requests

SERVER_IP = "0.0.0.0" #IP
API_SERVER = "https://2ddb-175-180-86-38.jp.ngrok.io" #port
DOWNLOAD_IMAGE_API = "/show-fsm"

try:
    downloadImageInfoResponse = requests.get(API_SERVER + DOWNLOAD_IMAGE_API)

    if downloadImageInfoResponse.status_code == 200:
        with open('img.jpg', 'wb') as getFile:
            getFile.write(downloadImageInfoResponse.content)
except Exception as err:
    print('Other error occurred %s' % {err})