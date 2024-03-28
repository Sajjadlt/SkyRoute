from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk,ImageGrab
import random

class Flight_card():
    def __init__(self,root,name,flight_iata_and_icao,origin,destination,date,time,flight_class) :
        self.path = filedialog.askdirectory() 
        window = Toplevel()
        window.title("for card :)")
        window.geometry("+0+0")
        window.attributes("-topmost","true")
        window.config(bg="#EAECE7")

        self.window = window

        base_image =ImageTk.PhotoImage(Image.open("images/ticket_base.png").resize((1000,457), Image.LANCZOS))
        base = Label(window,image=base_image ,text="")
        base.pack()
        base.PhotoImage = base_image

        name1 = Label(base,text=name,bg = "#EAECE7",font=("",14))
        name1.place(x = 110 , y = 150)

        name2 = Label(base,text=name,bg = "#EAECE7",font=("",14))
        name2.place(x = 740 , y = 140)

        flight1 = Label(base,text=flight_iata_and_icao,bg = "#EAECE7",font=("",12))
        flight1.place(x = 320 , y = 150)

        flight2 = Label(base,text=flight_iata_and_icao,bg = "#EAECE7",font=("",12))
        flight2.place(x = 740 , y = 245)

        seat = self.generate_random_seat_code()

        seat1 = Label(base,text=seat,bg = "#EAECE7",font=("",15))
        seat1.place(x = 625 , y = 150)

        seat2 = Label(base,text=seat,bg = "#EAECE7",font=("",15))
        seat2.place(x = 935 , y = 380)

        date1 = Label(base,text=date,bg = "#EAECE7",font=("",12))
        date1.place(x = 490 , y = 150)

        date2 = Label(base,text=date,bg = "#EAECE7",font=("",12))
        date2.place(x = 900 , y = 245)

        time1 = Label(base,text=time,bg = "#EAECE7",font=("",19),fg = "red")
        time1.place(x = 350 , y = 310)

        time2 = Label(base,text=time,bg = "#EAECE7",font=("",12))
        time2.place(x = 900 , y = 310)    

        gate = random.randint(10, 99)

        gate1 = Label(base,text=gate,bg = "#EAECE7",font=("",16))
        gate1.place(x = 780 , y = 315) 

        gate2 = Label(base,text=gate,bg = "#EAECE7",font=("",16))
        gate2.place(x = 110 , y = 315) 

        from1 = Label(base,text=origin,bg = "#EAECE7",font=("",13))
        from1.place(x = 170 , y = 190) 

        from1 = Label(base,text=origin,bg = "#EAECE7",font=("",13))
        from1.place(x = 800 , y = 170) 

        to1 = Label(base,text=destination,bg = "#EAECE7",font=("",13))
        to1.place(x = 170 , y = 220) 

        to2 = Label(base,text=destination,bg = "#EAECE7",font=("",13))
        to2.place(x = 800 , y = 195)

        self.code = self.generate_code()

        cod1 = Label(base,text=self.code,bg = "#EAECE7",font=("",13))
        cod1.place(x = 170 , y = 385) 

        cod2 = Label(base,text=self.code,bg = "#EAECE7",font=("",13))
        cod2.place(x = 790 , y = 390)

        class1 = Label(base,text=flight_class,bg = "#EAECE7",font=("",13,"bold"))
        class1.place(x = 600 , y = 90) 

        class2 = Label(base,text=flight_class,bg = "#EAECE7",font=("",13,"bold"))
        class2.place(x = 870 , y = 90) 

        self.window.after(300,self.screen)

        self.window.after(600,self.distroy)

    def screen(self):
        bbox = (10, 40, 1260, 615)
        im = ImageGrab.grab(bbox)
        if self.path:
            im.save(f'{self.path}/{self.code}.png')

        
    def distroy(self):
        self.window.destroy()

    def generate_random_seat_code(self):
        num = random.randint(10, 99)
        char = random.choice(["A","B","C"])
        return str(num) + char
    
    def generate_code(self):
        num = ""
        num += str(random.randint(1,9)) 
        for i in range(12):
            num += str(random.randint(0,9))
        return num

if __name__ == "__main__":
    Root = Tk()
    x = Flight_card(Root,"sajjad 510","WY5769/OMA5769", "IST/LTFM", "MCT/OOMS" ,"2024-02-25" ,"06:50:00","First Class")
    Root.mainloop()
    