import tkinter as tk
import json
from App.HTTPConnection import HTTPConnection
from App.Transport import config
from Transport.UITransport import *


class MyApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My App")
        f = open('ui-help-message.txt', 'r')
        temp = "".join(f.readlines())
        f.close()
        self.help_message = temp
        self.state = 'INIT'
        self.un = None
        self.urls = {}
        self.http = HTTPConnection()
        self.transport_config = config.Config.get_instance()
        self.rec, self.snd = None, None
        self.response = None
        self.target_peer_ip = None
        self.all_peers = None
        self.create_widgets()
        self.construct_urls()

    def construct_urls(self):
        f = open('url.json', 'r')
        temp = json.load(f)
        f.close()
        base_url = f'http://{temp["HTTP-HOST"]}:{temp["HTTP-PORT"]}'
        self.urls['SIGNUP'] = base_url + temp['SIGNUP']
        self.urls['GETPEERIP'] = base_url + temp['GETPEERIP']
        self.urls['GETALL'] = base_url + temp['GETALL']

    def new_rec(self):
        self.rec = UIReceiver(host=self.transport_config.config['HOST'],
                              handshake_port=self.transport_config.config['HANDSHAKE-PORT'])

    def new_snd(self):
        self.snd = UISender()

    def end_handshaking(self):
        self.target_peer_ip, self.rec, self.snd = None, None, None

    def set_target_peer_ip(self, ip):
        self.target_peer_ip = ip

    def wait_for_request(self):
        self.new_rec()
        self.rec.run()
        self.end_handshaking()

    def send_request(self, ip):
        self.set_target_peer_ip(ip)
        self.new_snd()
        self.snd.run(address=(ip, self.transport_config.config['HANDSHAKE-PORT']))
        self.end_handshaking()

    def error_scene(self, err):
        pass

    def init_program(self):
        pass

    def create_widgets(self):
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(side='bottom')
        self.textbox_frame = tk.Frame(self.window)
        self.textbox_frame.pack(anchor='center', pady=100)
        self.help_button = tk.Button(self.button_frame, text="Help", command=self.show_help)

        self.get_peers_button = tk.Button(self.button_frame, text="Get All Peers", command=self.get_all_peers)

        self.get_peer_ip_button = tk.Button(self.button_frame, text='Get Peer Ip', command=self.get_peer_ip)
        self.signup_button = tk.Button(self.button_frame, text="Sign Up", command=self.show_signup)

        self.wait_button = tk.Button(self.button_frame, text="Wait for Requests", command=self.wait_for_requests)

        self.send_request_button = tk.Button(self.button_frame, text="Send Request", command=self.show_send_request)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.window.quit)

        self.scene_frame = tk.Frame(self.window)
        self.scene_frame.pack(pady=20)

        self.label = tk.Label(self.scene_frame, text="")
        self.label.pack(anchor="center")

        self.button_back = tk.Button(self.button_frame, text='back', command=self.back)
        self.textbox_lable = tk.Label(self.textbox_frame, text='username: ')
        self.textbox_lable.pack(side='left', anchor='n')
        self.textbox = tk.Entry(self.textbox_frame)
        self.textbox.pack(anchor='center')
        self.send_bottun = tk.Button(self.textbox_frame, text='send', command=self.send_http)
        self.send_bottun.pack(side='top')

    def back(self):

        if self.state == 'O':
            self.label.config(text='')
            self.state = 'MAIN'
            self.button_back.pack_forget()

        elif self.state == 'SIGNUP':
            self.textbox_lable.pack_forget()
            self.textbox.pack_forget()
            self.send_bottun.pack_forget()
            self.button_back.pack_forget()
            self.state = 'MAIN'
        elif self.state == 'GETALL':
            self.label.config(text='')
            self.button_back.pack_forget()
            self.state = 'MAIN'

    def pack_main_menu_buttons(self):
        self.exit_button.pack(side='left', padx=10)
        self.help_button.pack(side='left', padx=10)
        self.signup_button.pack(side='left', padx=10)
        self.get_peers_button.pack(side='left', padx=10)
        self.wait_button.pack(side='left', padx=10)
        self.send_request_button.pack(side='left', padx=10)
        self.get_peer_ip_button.pack(side='left', padx=10)

    # def pack_forget_all(self):
    #     if self.state == 'MAIN':
    #         self.exit_button.pack_forget()
    #         self.help_button.pack_forget()
    #         self.signup_button.pack_forget()
    #         self.get_peers_button.pack_forget()
    #         self.wait_button.pack_forget()
    #         self.send_request_button.pack_forget()
    #         self.get_peer_ip_button.pack_forget()
    #     if self.state == '':
    #         pass

    def signup(self, un, ip, SHOW_MESSAGE=False):
        if self.state != 'MAIN' or self.state != 'INIT':
            self.back()
        self.response = json.loads(self.http.post(self.urls['SIGNUP'], json={'username': un, 'ip': ip}).text)

        if SHOW_MESSAGE:
            self.label.config(text=self.response['message'])
            self.back()
        if self.state != 'INIT':
            self.state = 'MAIN'
        print(self.state)

    def send_http(self):

        self.inp = self.textbox.get()
        self.send_bottun.pack_forget()
        self.textbox.pack_forget()
        self.textbox_lable.pack_forget()
        # self.textbox_lable.config(text='waiting for server response' if self.state != 'INIT' else 'initializing program...')

        if self.state == 'SIGNUP' or self.state == 'INIT':
            self.signup(self.inp, self.transport_config.config['HOST'], SHOW_MESSAGE=self.state == 'SIGNUP')
        if self.state == 'GETPEERIP':
            pass

        if self.state == 'INIT':
            self.get_all_peers()
            self.pack_main_menu_buttons()
            self.state = 'MAIN'
        # self.pack_main_menu_buttons()

    def get_peer_ip(self):
        self.label.config(text='get peer ip')
        self.state = 'O'
        self.button_back.pack(anchor='center')

    def show_help(self):
        self.label.config(text=self.help_message)
        self.state = 'O'
        self.button_back.pack(anchor='center')

    def get_all_peers(self):
        if self.state == 'GETALL':
            return
        if self.state == 'INIT':
            self.response = json.loads(self.http.get(self.urls['GETALL']).text)
            self.all_peers = self.response['all']
        else:
            if self.state != 'MAIN':
                self.back()

            self.response = json.loads(self.http.get(self.urls['GETALL']).text)
            self.all_peers = self.response['all']
            allpeerstxt = ''
            for x in self.all_peers:
                allpeerstxt += f'--\t\t{x:25}\n'
            self.label.config(text=allpeerstxt)
            self.button_back.pack(anchor='center')
            self.state = 'GETALL'
        print(self.state)

    def show_signup(self):
        if self.state == 'SIGNUP':
            return
        self.textbox_lable.pack(side='left', anchor='n')
        self.textbox.pack(anchor='center')
        self.send_bottun.pack(side='top')
        self.label.config(text='')
        if self.state != 'MAIN':
            self.back()
        self.state = 'SIGNUP'
        self.button_back.pack(anchor='center')

    def wait_for_requests(self):
        self.label.config(text="Wait for Requests scene")
        self.state = 'O'
        self.button_back.pack(anchor='center')

    def show_send_request(self):
        self.label.config(text="Send Request scene")
        self.state = 'O'
        self.button_back.pack(anchor='center')

    def run(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        window_x = int((screen_width - window_width) / 2)
        window_y = int((screen_height - window_height) / 2)
        self.window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        self.window.mainloop()


app = MyApp()
app.run()
