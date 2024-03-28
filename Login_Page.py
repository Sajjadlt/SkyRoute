from tkinter import *
from PIL import ImageTk, Image
from customtkinter import *
from tkinter import messagebox
import random
import smtplib
from email.mime.text import MIMEText
import mysql.connector

from App import App_user

sender_email ="  "#enter an email to send a verification code
password =  "  "#along with its password or thirdparty code

#××××××××××××××××××××××××××××× important ×××××××××××××××××××××××××××××
'''
The main code of this program is App
For this login, a database must be created in MySQL
Will be added in the future :)
'''

mydb = mysql.connector.connect(
  host="localhost",
  user=" root",
  password="",
  database = "skyroute"
)
curser = mydb.cursor()

class AuthenticationSystem_login():
    def __init__(self):
        self.user_data = {}
        

    def load_data(self):
        pass

    def login(self, username, password):
        curser.execute(f"Select * from login")
        users = curser.fetchall()
        for user in users:
            if user[1] == username and user[2] == password:
                return True
        return False

    def signup(self, username, password):
        curser.execute(f"Select * from login")
        users = curser.fetchall()
        for user in users:
            if user[1] == username:
                return False
        curser.execute(f"Insert into login(email,pass) values('{username}','{password}')",)
        mydb.commit()
        return True
        
    def chenge_pass(self, username, password):
        curser.execute(f"Select * from login where email='{username}'")
        user = curser.fetchone()
        if user == None:
            return False
        else:
            curser.execute(f"Update login set pass='{password}'  where email='{username}'")
            mydb.commit()
            return True
                       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LoginPage(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x550+350+150")
        self.title("Login page")
        self.resizable(False,False)

        self.auth_system = AuthenticationSystem_login()

        self.fram()
        self.login_frame_1()
        self.login_frame_2()

    def Signup(self):
        self.withdraw()
        singup_page = SingupPage(self)
        singup_page.mainloop()

    def Login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.auth_system.login(username, password):
            self.destroy()
            app = Tk(className="Sky Route")
            app.geometry("1536x800+0+0")
            #app.state('zoomed')
            #app.resizable(0,0)
            App_user(app)
            app.mainloop()
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password')

    def login_frame_1(self):
        CTkLabel(self.main_frame,width=385,text="WELCOME BACK",bg_color="#252525",text_color="#ffffff",font=('Segoe Script', 25, "bold")).place(anchor=NW, x=0, y=15)
        app_info_text = '''your app info\n...\n...\n...'''
        CTkLabel(self.main_frame,width=385,height=40,text=app_info_text,font=('yu gothic ui', 12)).place(anchor=NW, x=0, y=60)

        photo = CTkImage(Image.open("images\\vector.png"), size=(380, 380))
        side_image_label = CTkLabel(self.main_frame, image=photo, bg_color="#252525",width=390,text="")
        side_image_label.image = photo
        side_image_label.place(anchor=NW, x=0, y=130)

        bisecting_line = Canvas(self.main_frame, width=2, height=500, bg="#ffffff", highlightthickness=0)
        bisecting_line.place(x=384, y=10) 

    def login_frame_2(self):
        frame = Frame(self.main_frame,bg="#252525",width=384,height=520)
        frame.place(anchor=NW, x=386, y=0)

        CTkLabel(frame,width=384,height=30,text="Sign In",bg_color="#252525",text_color="#ffffff",font=('yu gothic ui', 20, "bold")).place(anchor=NW, x=0, y=110)

        CTkLabel(frame, width=384,image=CTkImage(Image.open("images\\hyy.png"), size=(114,80)),text="").place(anchor=NW, x=0, y=20)
        CTkLabel(frame,text="Username",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=153)
        CTkLabel(frame,text="(Enter your email)",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 10)).place(anchor=NW, x=115, y=154)
        CTkLabel(frame, image=CTkImage(Image.open("images\\username_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=180)
        self.username_entry = Entry(frame,width=45,insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.username_entry.place(anchor=NW, x=65, y=185)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=210)
        
        CTkLabel(frame,text="PassWord",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=233)
        CTkLabel(frame, image=CTkImage(Image.open("images\\password_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=260)
        self.password_entry = Entry(frame,width=40,show="*",insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.password_entry.place(anchor=NW, x=65, y=265)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=290)

        self.pass_status = False
        self.pass_status_bt = CTkButton(frame,width=20,height=20,image=CTkImage(Image.open("images\\hide.png"), size=(20,20)),text="", cursor='hand2',fg_color="#252525",hover_color="#252525",command=self.password_show_status)
        self.pass_status_bt.place(anchor=NW, x=310, y=260)

        Button(frame,width=20, text="Forgot Password ?",font=("yu gothic ui", 8, "bold underline"), fg="#C6C6C6", relief=FLAT,activebackground="#252525", borderwidth=0, background="#252525", cursor="hand2",command=self.forgot_Password_page).place(anchor=NW, x=130, y=310)

        self.login_bt = CTkButton(frame,width=185,height=27,text=">> LOGIN <<",font=('yu gothic ui', 18, "bold"), cursor='hand2',command=self.Login)
        self.login_bt.place(anchor=NW, x=100, y=340)

        signup_icon = Image.open('images\\register.png')
        signup_photo = ImageTk.PhotoImage(signup_icon,size=(45,15))
        self.signup_bt = Button(frame,command=self.Signup,relief=FLAT,image=signup_photo, cursor='hand2',bg="#252525",background="#252525",activebackground="#252525", borderwidth=0)
        self.signup_bt.image = signup_photo
        self.signup_bt.place(anchor=NW, x=180, y=380)
        Label(frame,text="No account yet ?",fg="#C6C6C6",bg="#252525").place(anchor=NW, x=90, y=390)

    def fram(self):
        first = Frame(self,width=800,height=550)
        first.pack()

        photo = CTkImage(Image.open("images\\background1.png"), size=(800, 550))
        CTkLabel(first, image=photo).place(anchor=NW, x=0, y=0)

        self.main_frame = Frame(master=first,width=770,height=520,bg="#252525")
        self.main_frame.place(anchor=NW, x=15, y=15)

    def password_show_status(self):
        if self.pass_status == False:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\show.png"), size=(20,20)))
            self.password_entry.config(show='')
            self.pass_status = True

        elif self.pass_status == True:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\hide.png"), size=(20,20)))
            self.password_entry.config(show='*')
            self.pass_status = False

    def forgot_Password_page(self):
        self.withdraw()
        forgot_Password_page = ForgotPasswordPage(self)
        forgot_Password_page.mainloop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

class SingupPage(Toplevel):
    def __init__(self,master):
        super().__init__()
        self.attributes("-topmost", True)
        self.title("SingUp Page")
        self.resizable(False,False)
        self.geometry("+350+150")

        self.auth_system = AuthenticationSystem_login()

        self.fram()
        self.singup_frame_1()
        self.singup_frame_2()

    def Singup(self):
        if (self.password_entry.get() == self.password_check_entry.get()) and (self.verification_code == self.verification_code_entry.get()):
            username = self.username_entry.get()
            password = self.password_entry.get()
            if self.auth_system.signup(username, password):
                self.master.deiconify()  
                self.destroy()  
                
            else:
                messagebox.showerror('Signup Failed', 'This email has already been registered')

        else:
            messagebox.showinfo('ERROR', f'Please fill out all the forms correctly\nSomething is wrong !!')

    def fram(self):
        first = Frame(self,width=800,height=550)
        first.pack()

        photo = CTkImage(Image.open("images\\background1.png"), size=(800, 550))
        CTkLabel(first, image=photo).place(anchor=NW, x=0, y=0)

        self.main_frame = Frame(master=first,width=770,height=520,bg="#252525")
        self.main_frame.place(anchor=NW, x=15, y=15)

    def singup_frame_1(self):
        CTkLabel(self.main_frame,width=385,text="WELCOME",bg_color="#252525",text_color="#ffffff",font=('Segoe Script', 25, "bold")).place(anchor=NW, x=0, y=10
                                                                                                                                           )
        app_info_text = '''your app info\n...\n...\n...'''
        CTkLabel(self.main_frame,width=385,height=40,text=app_info_text,font=('yu gothic ui', 12)).place(anchor=NW, x=0, y=60)

        photo = CTkImage(Image.open("images\\singup_vector.png"), size=(340, 340))
        side_image_label = CTkLabel(self.main_frame, image=photo, bg_color="#252525",width=350,text="")
        side_image_label.place(anchor=NW, x=20, y=145)

        bisecting_line = Canvas(self.main_frame, width=2, height=500, bg="#ffffff", highlightthickness=0)
        bisecting_line.place(x=384, y=10) 

    def singup_frame_2(self):
        frame = Frame(self.main_frame,bg="#252525",width=384,height=520)
        frame.place(anchor=NW, x=386, y=0)

        CTkLabel(frame,width=384,height=30,text="Sign Up",bg_color="#252525",text_color="#ffffff",font=('yu gothic ui', 20, "bold")).place(anchor=NW, x=0, y=20)

        CTkLabel(frame,text="Username",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=73)
        CTkLabel(frame,text="(Enter your email)",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 10)).place(anchor=NW, x=115, y=74)
        CTkLabel(frame, image=CTkImage(Image.open("images\\username_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=100)
        self.username_entry = Entry(frame,width=45,insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.username_entry.place(anchor=NW, x=65, y=105)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=130)
        
        CTkLabel(frame,text="PassWord",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=153)
        CTkLabel(frame, image=CTkImage(Image.open("images\\password_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=180)
        self.password_entry = Entry(frame,width=40,show="*",insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.password_entry.place(anchor=NW, x=65, y=185)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=210)
        self.pass_status = False
        self.pass_status_bt = CTkButton(frame,width=20,height=20,image=CTkImage(Image.open("images\\hide.png"), size=(20,20)),text="", cursor='hand2',fg_color="#252525",hover_color="#252525",command=self.password_show_status)
        self.pass_status_bt.place(anchor=NW, x=310, y=180)

        CTkLabel(frame,text="PassWord Check",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=233)
        CTkLabel(frame, image=CTkImage(Image.open("images\\password_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=260)
        self.password_check_entry = Entry(frame,width=40,show="*",insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.password_check_entry.place(anchor=NW, x=65, y=265)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=290)

        self.verification_code = "error"
        CTkLabel(frame,text="Verification code",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=313)
        CTkLabel(frame,text="(Click and check your email)",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 10)).place(anchor=NW, x=170, y=314)
        CTkLabel(frame, image=CTkImage(Image.open("images\\@.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=340)
        self.verification_code_entry = Entry(frame,width=40,insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.verification_code_entry.place(anchor=NW, x=65, y=345)
        CTkButton(frame,width=20,height=20,image=CTkImage(Image.open("images\\send.png"), size=(25,25)),text="", cursor='hand2',fg_color="#252525",hover_color="#151515",command=self.send_mail).place(anchor=NW, x=310, y=340)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=370)

        self.singup_bt = CTkButton(frame,width=185,height=35,text=">> CREATE AN ACCOUNT <<",font=('yu gothic ui', 18, "bold"), cursor='hand2',command=self.Singup)
        self.singup_bt.place(anchor=NW, x=65, y=400)

        CTkButton(frame,text = "cancel".upper() , fg_color="#871515" , bg_color="#252525",hover_color="#8C2A2A",command=self.cancel).place(anchor=NW, x=125, y=450)

    def cancel(self):
        self.master.deiconify()  
        self.destroy() 

    def password_show_status(self):
        if self.pass_status == False:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\show.png"), size=(20,20)))
            self.password_entry.config(show='')
            self.pass_status = True

        elif self.pass_status == True:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\hide.png"), size=(20,20)))
            self.password_entry.config(show='*')
            self.pass_status = False

    def send_mail(self):
        random_number = ''.join(random.choices('0123456789', k=6))
        self.verification_code = str(random_number)
        print(self.verification_code)

        if self.username_entry.get() == "":
            messagebox.showinfo('ERROR', f'Entr your mail !!!')
        else:
            message = f"\nHELLO\n\n\nyour code : {self.verification_code}"

            smtp_server = "smtp-mail.outlook.com"
            port = 587

            msg = MIMEText(message, 'plain')
            msg['Subject'] = "Test Message"
            msg['From'] = sender_email
            msg['To'] = self.username_entry.get()

            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

class ForgotPasswordPage(Toplevel):
    def __init__(self,master):
        super().__init__()
        self.attributes("-topmost", True)
        self.title("Forgot Password Page")
        self.resizable(False,False)

        self.auth_system = AuthenticationSystem_login()

        self.fram()
        
    def fram(self):
        first = Frame(self,width=415,height=550)
        first.pack()

        photo = CTkImage(Image.open("images\\background1.png"), size=(415, 550))
        CTkLabel(first, image=photo).place(anchor=NW, x=0, y=0)

        frame = Frame(master=first,width=385,height=520,bg="#252525")
        frame.place(anchor=NW, x=15, y=15)

        CTkLabel(frame, width=100,image=CTkImage(Image.open("images\\forgot_pass.png"), size=(100,100)),text="").place(anchor=NW, x=250, y=20)

        CTkLabel(frame,height=30,text="Forgot PassWord",bg_color="#252525",text_color="#ffffff",font=('yu gothic ui', 20, "bold")).place(anchor=NW, x=40, y=50)
       
        CTkLabel(frame,text="Username",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=113)
        CTkLabel(frame,text="(Enter your email)",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 10)).place(anchor=NW, x=115, y=114)
        CTkLabel(frame, image=CTkImage(Image.open("images\\username_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=140)
        self.username_entry = Entry(frame,width=45,insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.username_entry.place(anchor=NW, x=65, y=145)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=170)

        CTkLabel(frame,text="PassWord",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=193)
        CTkLabel(frame, image=CTkImage(Image.open("images\\password_icon.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=220)
        self.password_entry = Entry(frame,width=40,show="*",insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.password_entry.place(anchor=NW, x=65, y=225)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=250)
        self.pass_status = False
        self.pass_status_bt = CTkButton(frame,width=20,height=20,image=CTkImage(Image.open("images\\hide.png"), size=(20,20)),text="", cursor='hand2',fg_color="#252525",hover_color="#252525",command=self.password_show_status)
        self.pass_status_bt.place(anchor=NW, x=310, y=220)

        self.verification_code = "error"
        CTkLabel(frame,text="Verification code",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 16, "bold")).place(anchor=NW, x=40, y=273)
        CTkLabel(frame,text="(Click and check your email)",bg_color="#252525",text_color="#686868",font=('yu gothic ui', 10)).place(anchor=NW, x=170, y=274)
        CTkLabel(frame, image=CTkImage(Image.open("images\\@.png"), size=(20,20)),text="").place(anchor=NW, x=40, y=300)
        self.verification_code_entry = Entry(frame,width=40,insertbackground="white",bg="#252525",relief=FLAT,fg="white")
        self.verification_code_entry.place(anchor=NW, x=65, y=305)
        CTkButton(frame,width=20,height=20,image=CTkImage(Image.open("images\\send.png"), size=(25,25)),text="", cursor='hand2',fg_color="#252525",hover_color="#151515",command=self.send_mail).place(anchor=NW, x=310, y=300)
        Canvas(frame, width=300, height=2, bg="#ffffff", highlightthickness=0).place(x=40, y=330)

        self.change_bt = CTkButton(frame,width=132,height=35,text="CHENGE",font=('yu gothic ui', 18, "bold"), cursor='hand2',command=self.Change_pass)
        self.change_bt.place(anchor=NW, x=40, y=350)

        CTkButton(frame,text = "cancel".upper() , fg_color="#871515" , bg_color="#252525",hover_color="#8C2A2A",command=self.cancel,width=132,height=35).place(anchor=NW, x=211, y=350)

    def Change_pass(self):
        if self.verification_code == self.verification_code_entry.get():
            if self.auth_system.chenge_pass(self.username_entry.get(),self.password_entry.get()) :
                self.master.deiconify()  
                self.destroy()  

            else:
                messagebox.showinfo('ERROR', f'Please fill out all the forms correctly\nSomething is wrong !!')

    def cancel(self):
        self.master.deiconify()  
        self.destroy() 

    def send_mail(self):
        random_number = ''.join(random.choices('0123456789', k=6))
        self.verification_code = str(random_number)

        if self.username_entry.get() == "":
            messagebox.showinfo('ERROR', f'Entr your mail !!!')
        else:
            message = f"\nHELLO\n\n\nyour code : {self.verification_code}"

            smtp_server = "smtp-mail.outlook.com"
            port = 587

            msg = MIMEText(message, 'plain')
            msg['Subject'] = "Test Message"
            msg['From'] = sender_email
            msg['To'] = self.username_entry.get()

            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()

    def password_show_status(self):
        if self.pass_status == False:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\show.png"), size=(20,20)))
            self.password_entry.config(show='')
            self.pass_status = True

        elif self.pass_status == True:
            self.pass_status_bt.configure(image=CTkImage(Image.open("images\\hide.png"), size=(20,20)))
            self.password_entry.config(show='*')
            self.pass_status = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Start():
    App = LoginPage()
    App.mainloop()

if __name__ == "__main__":
    Start()
