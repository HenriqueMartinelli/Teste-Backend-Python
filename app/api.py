from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer

app = Flask(__name__)
socketio = SocketIO(app)

bootstrap_servers = 'localhost:9092'
topic = 'kafta_teste'

def get_kafka_messages_and_notify():
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id='viewer-group')
    for message in consumer:
        message_value = message.value.decode()
        socketio.emit('new_message', message_value)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.start_background_task(get_kafka_messages_and_notify)  
    socketio.run(app, debug=True)