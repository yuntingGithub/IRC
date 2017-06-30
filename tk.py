# -*- coding:utf-8 -*-

from telnetlib import *
import thread
import sys

from mtTkinter import *
host = "127.0.0.1"
port = 5000

server = Telnet(host, port)

def position(self):
    self.master.withdraw()  # 隐藏，不在界面显示部件，然后获取部件所在界面的尺寸
    self.screen_width = self.master.winfo_screenwidth()
    self.screen_height = self.master.winfo_screenheight()
    self.master.resizable(True,True) 
    self.master.update_idletasks()   # 显示正常窗口的关键语句
    self.master.deiconify()   # 重新显示
    self.master.withdraw() # TK
    self.master.geometry('%sx%s+%s+%s' %
            (
            self.master.winfo_width() ,
            self.master.winfo_height() ,
            (self.screen_width - self.master.winfo_width())/2,
            (self.screen_height - self.master.winfo_height())/2
            ))  # TK
    self.master.deiconify()





class Welcome(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.welcome()
        self.master.title('网络聊天室') # 要放在定位之前……
        position(self)

    def get_name(self, event):
        name = self.source.get()
        keyd = self.keyword.get()
        userw=name+" "+keyd
        server.write("/login " + userw + "\r\n")
        s = server.read_until("More helps use: /help", 1)
        if "Please try again." in s:
            self.info["text"] = "该账户已经登录，请退出后再操作"
        elif "wrong." in s:
            self.info["text"] = "账号或密码错误，请重新输入"
        else:
            root = Tk()
            app = Chat(master=root)
            self.master.destroy() # 销毁此组件 和 其子组件


    def get_key(self,event):
        key=self.keys.get()
        server.write("/keys"+key+"\r\n")
        

    def welcome(self):
        self.inputText = Label(self)
        self.inputText["text"] = "欢迎登录:"
        self.inputText.pack(side="top")

        self.info = Label(self)
        self.info["text"] = "用户名"
        self.info.pack(side="top")
        
        self.source = StringVar()
        self.input_name = Entry(self, textvariable=self.source)
        self.input_name["width"] = 20
        self.input_name.bind('<Return>', self.get_name)
        self.input_name.pack(side="top", ipadx=35, padx=35,pady=10)

        self.info2= Label(self)
        self.info2["text"] = "密码"
        self.info2.pack(side='top')

        self.keyword=StringVar()
        self.keys = Entry(self, textvariable=self.keyword)
        self.keys["width"] = 20
        self.keys.bind('<Return>', self.get_name)
        self.keys.pack(side="left", ipadx=35, padx=35,pady=10)


class Chat(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.chatroom()
        self.master.title('IRC')
        position(self)

    def room_python(self):
        root = Tk()
        app = Room(master=root, name="python")
        app.startNewThread()
        self.master.destroy()

    def room_write(self):
        root = Tk()
        app = Room(master=root, name="write")
        app.startNewThread()
        self.master.destroy()

    def room_pm(self):
        root = Tk()
        app = Room(master=root, name="pm")
        app.startNewThread()
        self.master.destroy()

    def chatroom(self):
        self.inputText = Label(self)
        self.inputText["text"] = "请选择聊天室进入:"
        self.inputText.pack(side="top")

        self.python = Button(self)
        self.python["text"] = "python学习"
        self.python["padx"] = 40
        self.python["command"] =  self.room_python
        self.python.pack(side="left")

        self.write = Button(self)
        self.write["text"] = "文学熏陶"
        self.write["padx"] = 40
        self.write["command"] =  self.room_write
        self.write.pack(side="left")

        self.pm = Button(self)
        self.pm["text"] = "午夜休闲"
        self.pm["padx"] = 40
        self.pm["command"] =  self.room_pm
        self.pm.pack(side="left")

class Room(Frame):

    def __init__(self, master=None, name=None):
        Frame.__init__(self, master)
        server.write("/"+name+"\r\n")
        self.pack() # 用来管理和显示组件，默认 side = "top"

        self.frame_l_t = Frame(self)
        self.frame_l_m = Frame(self)
        self.frame_l_b = Frame(self)
        self.frame_r = Frame(self)

        self.QUIT = Button(self.frame_l_b)
        self.QUIT["text"] = "退出"
        self.QUIT["fg"]   = "black"
        self.QUIT["padx"] = 40
        self.QUIT["command"] =  self.master.destroy
        self.QUIT.pack(side="left")
        
        self.back = Button(self.frame_l_b)
        self.back["text"] = "返回"
        self.back["fg"]   = "black"
        self.back["padx"] = 40
        self.back["command"] =  self.back_hall
        self.back.pack(side="left")
        
        self.online = Button(self.frame_l_b)
        self.online["text"] = "在线用户"
        self.online["padx"] = 40
        self.online["command"] = self.online_people
        self.online.pack(side="right")
        self.frame_l_b.pack()
        
        self.scrollbar = Scrollbar(self.frame_l_t)
        self.chatText = Listbox(self.frame_l_t, width=70, height=18, yscrollcommand=self.scrollbar.set,background='gray')
        self.chatText.yview_moveto(1.0)
        self.scrollbar.config(command=self.chatText.yview)
        self.scrollbar.pack(side="right", fill=Y)
        self.chatText.pack(side="left")
        self.frame_l_t.pack()
        
        self.message_input = StringVar()
        self.message_send = Entry(self.frame_l_m, textvariable=self.message_input)
        self.message_send["width"] = 70
        self.message_send.bind('<Return>', self.send_message)
        self.message_send.pack(fill=X)
        self.frame_l_m.pack()


        self.master.title(name)
        position(self)
        self.chatText.insert(END, server.read_until("!"))


    def receiveMessage(self):
        socket = server.get_socket()
        while 1:
            clientMsg = socket.recv(4096)       #接受数据
            if not clientMsg:
                continue
            else:
                self.chatText.insert(END, clientMsg)
                self.chatText.yview_moveto(1.0)

    def startNewThread(self):
        thread.start_new_thread(self.receiveMessage, ())


    def online_people(self):
        server.write("/online" + "\r\n")

    def send_message(self, event):
        send_mesg = self.message_input.get().strip(" ")
        if send_mesg:
            server.write(send_mesg.encode("utf-8")+"\r\n")
            self.chatText.yview_moveto(1.0)
            self.message_send.delete(0, END)
        else:
            self.chatText.insert(END, "<不能发送空消息>")
            self.chatText.yview_moveto(1.0)
            self.message_send.delete(0, END)

    def back_hall(self):
        server.write("/back" + "\r\n")
        root = Tk()
        app = Chat(master=root)
        self.master.destroy()

    def offline(self):
        server.write("/logout\r\n")
        sys.exit()


# 创建一个根窗口

root = Tk()
app = Welcome(master=root)

root.mainloop()
