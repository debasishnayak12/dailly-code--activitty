# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import websocket
import json
import time

class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.chat_log = ScrollView(size_hint=(1, 0.8))
        self.chat_log_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_log_content.bind(minimum_height=self.chat_log_content.setter('height'))
        self.chat_log.add_widget(self.chat_log_content)

        self.add_widget(self.chat_log)

        self.message_input = TextInput(size_hint=(0.8, 0.3), multiline=False)
        self.send_button = Button(text="Send", size_hint=(0.2, 0.2))
        self.send_button.bind(on_press=self.send_message)

        input_box = BoxLayout(size_hint=(1, 0.1))
        input_box.add_widget(self.message_input)
        input_box.add_widget(self.send_button)

        self.add_widget(input_box)

        self.ws = None
        self.connect_to_server()

    def connect_to_server(self):
        def run(*args):
            while True:
                try:
                    self.ws = websocket.WebSocketApp(
                        "ws://192.168.1.77:5000/socket.io/?EIO=4&transport=websocket",
                        on_message=self.on_message,
                        on_error=self.on_error,
                        on_close=self.on_close
                    )
                    self.ws.on_open = self.on_open
                    self.ws.run_forever()
                except Exception as e:
                    print(f"Error connecting to WebSocket: {e}")
                time.sleep(5)  # Reconnect after 5 seconds if connection is lost

        threading.Thread(target=run).start()

    def on_open(self, ws):
        print("WebSocket connection opened")

    def on_message(self, ws, message):
        print(f"Raw message received: {message}")
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        Clock.schedule_once(lambda dt: self.update_chat_log(data), 0)


    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket connection closed: {close_status_code}, {close_msg}")

    def update_chat_log(self, message):
        self.chat_log_content.add_widget(Label(text=message, size_hint_y=None, height=40))

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            try:
                self.ws.send(json.dumps(message))
                self.message_input.text = ''
                self.update_chat_log(f"You: {message}")
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket connection is closed. Unable to send message.")

class MessagingApp(App):
    def build(self):
        return ChatScreen()

if __name__ == '__main__':
    MessagingApp().run()
