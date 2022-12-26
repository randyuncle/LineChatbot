import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv() 

machine = TocMachine(
    states=["user", "information", "input_rating_area", "input_rating_item", "input_popular_area", "input_popular_item", "print_rating_list", "print_popular_list"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "information",
            "conditions": "is_going_to_information",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "input_rating_area",
            "conditions": "is_going_to_input_rating_area",
        },
        {
            "trigger": "advance",
            "source": "input_rating_area",
            "dest": "input_rating_item",
            "conditions": "is_going_to_input_rating_item",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "input_popular_area",
            "conditions": "is_going_to_input_popular_area",
        },
        {
            "trigger": "advance",
            "source": "input_popular_area",
            "dest": "input_popular_item",
            "conditions": "is_going_to_input_popular_item",
        },
        {
            "trigger": "advance",
            "source": "input_rating_item",
            "dest": "print_rating_list",
            "conditions": "is_going_to_print_rating_list",
        },
        {
            "trigger": "advance",
            "source": "input_popular_item",
            "dest": "print_popular_list",
            "conditions": "is_going_to_print_popular_list",
        },
        {"trigger": "go_back", "source": ["information", "input_rating_area", "input_rating_item", "input_popular_area", "input_popular_item", "print_rating_list", "print_popular_list"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state != 'user' and event.message.text.lower() == 'reset':
                send_text_message(event.reply_token, "已回到開頭!\n輸入\"information\"：顯示本機器人的詳細資訊。\n輸入\"rating\"：本機器人會以「評分」的高低來為您篩選前10推薦餐廳。\n輸入\"popular\"：本機器人會以「人氣」的高低來為您篩選前10推薦餐廳。\n隨意時間輸入\"reset\"：重頭開始")
                machine.go_back()
            elif machine.state == 'user' and event.message.text.lower() == 'reset':
                send_text_message(event.reply_token, "您現在已在初始狀態\n輸入\"information\"：顯示本機器人的詳細資訊。\n輸入\"rating\"：本機器人會以「評分」的高低來為您篩選前10推薦餐廳。\n輸入\"popular\"：本機器人會以「人氣」的高低來為您篩選前10推薦餐廳。")
            else:
                send_text_message(event.reply_token, "!請依照功能的說明進行操作!")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
