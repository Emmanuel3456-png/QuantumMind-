from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import webbrowser
from Brain import process_command, banner
from database import load_users, save_users, hash_pass

Window.clearcolor=(0.02,0.04,0.10,1)
class QMApp(App):
    title='Quantum Mind'
    def build(self): self.username=None; self.role=None; return self.login_screen()
    def label(self,text,size=18): return Label(text=text,font_size=dp(size),color=(0.8,0.9,1,1))
    def login_screen(self):
        root=BoxLayout(orientation='vertical',padding=dp(24),spacing=dp(12))
        root.add_widget(self.label('[b]QUANTUM MIND[/b]\nSoftnet Technology Academy',28))
        self.user=TextInput(hint_text='Username',multiline=False,size_hint_y=None,height=dp(52))
        self.password=TextInput(hint_text='Password',password=True,multiline=False,size_hint_y=None,height=dp(52))
        msg=self.label('',14); root.add_widget(self.user); root.add_widget(self.password)
        b=Button(text='LOGIN',size_hint_y=None,height=dp(54)); b.bind(on_release=lambda *_:self.do_login(msg)); root.add_widget(b); root.add_widget(msg)
        return root
    def do_login(self,msg):
        u=self.user.text.strip().lower(); p=self.password.text
        data=load_users().get(u)
        if data and data.get('password') in (p,hash_pass(p)):
            self.username=u; self.role=data.get('role','user').lower(); self.root.clear_widgets(); self.root.add_widget(self.chat_screen())
        else: msg.text='Access denied. Authorized school users only.'
    def chat_screen(self):
        root=BoxLayout(orientation='vertical',padding=dp(10),spacing=dp(8))
        top=BoxLayout(size_hint_y=None,height=dp(48)); top.add_widget(self.label(f'Quantum Mind  •  {self.username} ({self.role})',16))
        if self.role=='admin':
            a=Button(text='Admin',size_hint_x=.28); a.bind(on_release=self.admin_popup); top.add_widget(a)
        root.add_widget(top)
        scroll=ScrollView(); self.chat=Label(text=banner()+'\n',size_hint_y=None,text_size=(Window.width-dp(30),None),valign='top',markup=True)
        self.chat.bind(texture_size=lambda inst,val:setattr(inst,'height',val[1]+dp(20))); scroll.add_widget(self.chat); root.add_widget(scroll)
        row=BoxLayout(size_hint_y=None,height=dp(58),spacing=dp(6)); self.entry=TextInput(hint_text='Ask Quantum Mind...',multiline=False); self.entry.bind(on_text_validate=self.send)
        send=Button(text='Send',size_hint_x=.25); send.bind(on_release=self.send); row.add_widget(self.entry); row.add_widget(send); root.add_widget(row); self.scroll=scroll
        return root
    def send(self,*_):
        text=self.entry.text.strip()
        if not text:return
        self.entry.text=''; result=process_command(text,self.username); self.chat.text+=f'\n[b]You:[/b] {text}\n[b]Quantum Mind:[/b] {result["text"]}\n'
        if result.get('url'):
            self.pending_url=result['url']; self.pending_source=result.get('source','Source'); self.chat.text+=f'[ref=source][u]Open source: {self.pending_source}[/u][/ref]\n'; self.chat.bind(on_ref_press=self.open_source)
        self.scroll.scroll_y=0
    def open_source(self,*_): webbrowser.open(self.pending_url)
    def admin_popup(self,*_):
        box=BoxLayout(orientation='vertical',padding=dp(10),spacing=dp(6)); info=self.label('Add an authorized user',16)
        u=TextInput(hint_text='Username',multiline=False); p=TextInput(hint_text='Password',password=True,multiline=False); r=TextInput(hint_text='Role: student / teacher / admin',multiline=False)
        status=self.label('',13); add=Button(text='Add / Update User',size_hint_y=None,height=dp(48))
        def save(*_):
            name=u.text.strip().lower(); role=r.text.strip().lower()
            if not name or not p.text or role not in ('student','teacher','admin','user'): status.text='Enter username, password and a valid role.'; return
            users=load_users(); users[name]={'password':hash_pass(p.text),'role':role}; save_users(users); status.text=f'{name} saved as {role}.'
        add.bind(on_release=save)
        for w in (info,u,p,r,add,status): box.add_widget(w)
        Popup(title='Quantum Mind Admin',content=box,size_hint=(.92,.75)).open()
if __name__=='__main__': QMApp().run()
