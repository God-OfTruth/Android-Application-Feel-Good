from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json,glob
import datetime,random
from pathlib import Path



Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users=json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text= "Wrong Username or Password"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

class SignUpScreen(Screen):

    def add_user(self,uname,pword):
        with open("users.json") as file:
            users=json.load(file)
        users[uname]={'username': uname,'password': pword,
        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users,json",'w')as file:
            json.dump(users,file)

        self.manager.current="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction="right"
        self.manager.current = "login"

    def get_quote(self,feeling):
        feel=feeling.lower()
        aval_feel=  glob.glob("quotes/*txt")
        aval_feel=[Path(filename).step for filename in aval_feel]
        if feel in aval_feel:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text='Try Another Feeling'

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

if __name__=="__main__":
    MainApp().run()
