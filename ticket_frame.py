from tkinter import * 
from customtkinter import *
from tkintermapview import *
from CTkListbox import *
import datetime
from PIL import Image, ImageTk
from tkinter import messagebox

from flight_card import Flight_card

class Ticket_frame():
    def __init__(self,frame,App = None):
        self.App = App

        frame.configure(  width=1000,height=550,border_width = 5,border_color = "#008ae6", bg_color= "#000000")

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ticket_frame = CTkFrame(frame,width=600,height=520,border_width=3 , border_color="#008ae6")
        ticket_frame.place(x = 15,y = 15)

        search_frame = CTkFrame(frame,width=370,height=520,border_width=3 , border_color="#008ae6")
        search_frame.place(x = 620,y = 15)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        buyer_info_frame = CTkFrame(ticket_frame,width=570,height=50)
        buyer_info_frame.place(x =15 , y = 15 )

        self.fname_entry = CTkEntry(buyer_info_frame,placeholder_text="First Name",border_color = "#008ae6",fg_color="#004d4d",width=150,font=("Arial",15))
        self.fname_entry.grid(row = 0 ,column = 0 ,padx = 10 , pady=10)

        self.lname_entry = CTkEntry(buyer_info_frame,placeholder_text="Last Name",border_color = "#008ae6",fg_color="#004d4d",width=150,font=("Arial",15))
        self.lname_entry.grid(row = 0 ,column = 1 ,padx = 10 , pady=10)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flight_info_frame = CTkFrame(ticket_frame,width=570,)
        flight_info_frame.place(x =15 , y = 73 )

        CTkLabel(flight_info_frame,font=("Arial",15) ,text="Origin : ",width=40).place(x = 45 , y = 15 )
        self.origin_entry = CTkEntry(flight_info_frame,placeholder_text="The icao of the airport of origin",border_color = "#008ae6",fg_color="#004d4d",width=250,font=("Arial",15))
        self.origin_entry.place(x =95 , y = 15 )

        CTkLabel(flight_info_frame,font=("Arial",15) ,text="destination : ",width=40).place(x = 15 , y = 55 )
        self.destination_entry = CTkEntry(flight_info_frame,placeholder_text="The icao of the destination airport",border_color = "#008ae6",fg_color="#004d4d",width=250,font=("Arial",15))
        self.destination_entry.place(x =95 , y = 55 )

        CTkLabel(flight_info_frame,font=("Arial",15) ,text="flight icao : ",width=40).place(x = 23 , y = 95 )
        self.flight_icao_entry = CTkEntry(flight_info_frame,placeholder_text="The icao of the flight",border_color = "#008ae6",fg_color="#004d4d",width=250,font=("Arial",15))
        self.flight_icao_entry.place(x =95 , y = 95 )

        description_lb = CTkLabel(flight_info_frame,justify = "left",text = "All the entries of this frame \nare filled with flights\n according to your choice\n except for some")
        description_lb.place(x = 370 , y =15)

        self.flight_info = CTkLabel(flight_info_frame,font=("",15),justify = "left",text = "flight date : ???\n\nflight time : ???")
        self.flight_info.place(x = 15 , y =130)

        self.flight_class = CTkComboBox(flight_info_frame,width=150,font=("",15), values=["Economy Class", "Premium Economy","Business Class","First Class"],button_hover_color="#008ae6",button_color="#008ae6",border_color="#008ae6")
        self.flight_class.place(x = 390 , y =100)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        button_frame = CTkFrame(ticket_frame,width=570)
        button_frame.place(x =60 , y = 453 )

        CTkButton(button_frame,command=self.clear , text = "Clear",font = ("",25),fg_color = "#737373",hover_color="#4d4d4d").grid(row = 0 ,column = 0,padx = 10 , pady = 10)
        CTkButton(button_frame,command=lambda : frame.destroy() , text = "Exit",font = ("",25),fg_color = "#cc0000",hover_color="#990000").grid(row = 0 ,column = 1,padx = 10 , pady = 10)
        CTkButton(button_frame,command=self.save_card , text = "Flight Card",font = ("",25),fg_color = "#2eb82e",hover_color="#1f7a1f").grid(row = 0 ,column = 2,padx = 10 , pady = 10)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.search_entry = CTkEntry(search_frame,border_color = "#008ae6",fg_color="#004d4d",width=340,font=("Arial",15))
        self.search_entry.pack(fill = X , padx = 15, pady = 15)

        self.list_box = CTkListbox(search_frame,command=self.get_data,width=308,height=415,border_color = "#008ae6",scrollbar_button_color = "#0099cc")
        self.list_box.pack( padx = 15, pady = 15)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.show_all(self.App.scheduled_flights)
        self.search_entry.bind("<KeyRelease>", self.Search)

    def get_data(self,Input):
        Icao = ""
        for i in Input[5:12]:
            if i == "" or i == "\t":
                continue
            Icao += i

        flights = self.App.scheduled_flights

        for flight in flights:
            if flight["flight"]["icao"] == Icao:
                self.origin_entry.delete(0,100)
                self.destination_entry.delete(0,100)
                self.flight_icao_entry.delete(0,100)

                self.origin_entry.insert(0,flight["arrival"]["icao"])
                self.destination_entry.insert(0,flight["departure"]["icao"])
                self.flight_icao_entry.insert(0,flight["flight"]["icao"])
                date = self.datetime_changer(flight["arrival"]["scheduled"])
                self.flight_info.configure(text=f"flight date : {date[0]}\n\nflight time : {date[1]}")
        
    def Search(self,input):
        s1 = self.search_entry.get().lower()
        if s1 == "" or s1 == " ":
            self.show_all(flights=self.App.scheduled_flights)
        else:
            flights = self.App.scheduled_flights
            number = 0
            self.list_box.delete("all")
            for flight in flights:
                if (flight["arrival"]["icao"][0:len(s1)]).lower() == s1:
                    self.list_box.insert(number,f"Icao:{flight["flight"]["icao"]}\tOrigin :{flight["arrival"]["icao"]}   Toward :{flight["departure"]["icao"]}")
                    number = number + 1

    def show_all(self,flights):
        number = 0
        self.list_box.delete("all")
        for flight in flights:
            self.list_box.insert(number,f"Icao:{flight["flight"]["icao"]}\tOrigin :{flight["arrival"]["icao"]}   Toward :{flight["departure"]["icao"]}")
            number = number + 1

    def save_card(self):
        s1 = self.flight_icao_entry.get()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        if s1 == "" and fname == "" and lname =="":
            messagebox.showwarning(title="Fill out the form!", message="To save the card, you must enter at least the first and last name and ICAO of one of the available flights" )
        else:
            flights = self.App.scheduled_flights
            x = False
            for flight in flights:
                if s1 == flight["flight"]["icao"]:
                    date = self.datetime_changer(flight["arrival"]["scheduled"])
                    Flight_card(root = self.App.root,name = f"{fname} {lname}",flight_iata_and_icao = f"{flight["flight"]["iata"]}/{flight["flight"]["icao"]}",origin = f"{flight["arrival"]["iata"]}/{flight["arrival"]["icao"]}",destination = f"{flight["departure"]["iata"]}/{flight["departure"]["icao"]}",date = date[0],time = date[1],flight_class = self.flight_class.get())
                    x = True
                if x :
                    break
            if x == False:
                messagebox.showerror(title="Error", message=f"Flight with this icao({s1}) is not available in the list!\nPlease use the available flights")

    def clear(self):
        self.fname_entry.delete(0,100)
        self.lname_entry.delete(0,100)
        self.origin_entry.delete(0,100)
        self.destination_entry.delete(0,100)
        self.flight_icao_entry.delete(0,100)
        self.flight_info.configure(text="flight date : ???\n\nflight time : ???")

    def datetime_changer(self,datetime_str):
        datetime_object = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
        return datetime_object.date(),datetime_object.time()


if __name__ == "__main__":
    app = Tk()
    my_frame = CTkFrame(app)
    my_frame.pack()
    Ticket_frame(frame = my_frame)
    app.mainloop()