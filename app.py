from flask import Flask, request, jsonify
from kubemq.events.lowlevel.event import Event
from kubemq.events.lowlevel.sender import Sender
import os

app = Flask(__name__)

def publish_event_to_kubemq(channel, body):
    event = Event(
        channel=channel,
        body=body,
        store=False,
    )

    sender = Sender(os.environ.get("KUBEMQ_SVC"))

    try:
        sender.send_event(event)
        print("Event sent successfully")
    except Exception as e:
        print(f"Failed to send event: {str(e)}")

@app.route('/', methods=['POST'])
def index():
    data = request.json
    publish_event_to_kubemq("test", data)
    return jsonify({"status": "received"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received Data: {data}")
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)