from tkinter import * 
from customtkinter import *
from tkintermapview import *
from CTkListbox import *
import datetime

class Search_frame():
    def __init__(self,frame,App = None):
        self.App = App
        frame.configure(  width=1000,height=550,border_width = 5,border_color = "#008ae6", bg_color= "#000000")

        CTkButton(frame ,command=lambda : frame.destroy(), text="x",font=("",30,"bold"),hover_color = "#2B2B2B",fg_color="#2B2B2B",bg_color = "#2B2B2B",width=20,text_color="#ffffff").place(x=960,y =5)

        CTkLabel(frame , text="Search By:",font=("",15)).place(x=30,y =20)

        self.search_type = CTkOptionMenu(frame,font=("",15), values=["Number", "Iata", "Icao","Ruote","Airline"],command=self.Search)
        self.search_type.place(x=120,y =20)

        CTkLabel(frame , text="Flight status: :",font=("",15)).place(x=280,y =20)

        self.search_list = CTkOptionMenu(frame,font=("",15), values=["active","scheduled","landed"],command=self.Search)
        self.search_list.place(x=390,y =20)

        self.search_entry = CTkEntry(frame,border_color = "#008ae6",fg_color="#004d4d",width=230,font=("Arial",15))
        self.search_entry.place(x=35,y =70)

        self.search_entry_2 = CTkEntry(frame,border_color = "#008ae6",fg_color="#004d4d",width=230,font=("Arial",15),)
        self.search_entry_2.place(x=290,y =70)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.list_box = CTkListbox(frame,border_color = "#008ae6",height=400,width=500,scrollbar_button_color = "#0099cc",command=self.get_data)
        self.list_box.place(x=30,y = 110)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        info_frame = CTkFrame(frame,width=395,height=470,border_width=3 , border_color="#008ae6")
        info_frame.place(x = 580 , y = 60)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        CTkLabel(info_frame,text = "" ,width=1 , height = 1).place(x = 394,y = 469)

        self.flight_info_label = CTkLabel(info_frame,text = "[Flight]\n\nFlight Number : ???\niata/icoa : ???/???\nStatus : ???",width=385)
        self.flight_info_label.place(x = 5 , y =10)

        self.departure_info_label = CTkLabel(info_frame,text = "[departure] \n\nAirport: ???\niata/icoa : ???/???\nLanding date : ???\nlanding time : ???",width=185)
        self.departure_info_label.place(x = 5 , y =120)

        self.arrival_info_label = CTkLabel(info_frame,text = "[arrival] \n\nAirport : ???\niata/icoa : ???/???\nTake off date : ???\nTake off time : ???",width=185)
        self.arrival_info_label.place(x = 190 , y =120)

        self.airline_info_label = CTkLabel(info_frame,text = "[Airline] \n\nName : ???\niata/icoa : ???/???",width=385)
        self.airline_info_label.place(x = 5 , y =360)

        self.show_map_bt = CTkButton(info_frame,text = "Show in map",width=125,font=("",15,"bold"),height=20,state="disabled")
        self.show_map_bt.place(x = (385-125)/2 , y =300)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.search_entry_2.configure(state="disabled")
        self.show_all(self.App.flights)
        self.search_entry.bind("<KeyRelease>", self.Search)
        self.search_entry_2.bind("<KeyRelease>", self.Search)

    def Search(self,input):
        s1 = self.search_entry.get().lower()
        type1 = self.search_type.get().lower()
        type2 = self.search_list.get().lower()
        if s1 != "":
            if type2 == "active":
                self.search_entry_2.configure(state="disabled")
                self.show_Search(self.App.flights,type1)
            elif type2 == "scheduled":
                self.search_entry_2.configure(state="disabled")
                self.show_Search(self.App.scheduled_flights,type1)
            elif type2 == "landed":
                self.search_entry_2.configure(state="disabled")
                self.show_Search(self.App.landed_flights,type1)

        else:
            if type2 == "active":
                self.show_all(self.App.flights)
            elif type2 == "scheduled":
                self.show_all(self.App.scheduled_flights)
            elif type2 == "landed":
                self.show_all(self.App.landed_flights)

    def show_Search(self,flights,sby):
        s1 = self.search_entry.get().lower()
        s2 = self.search_entry_2.get().lower()
        if sby == "Number".lower():
            self.search_entry_2.configure(state="disabled")
            number = 0
            self.list_box.delete("all")
            for flight in flights:
                if flight["flight"]["number"][0:len(s1)] == s1:
                    self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
                    number = number + 1

        elif sby == "Iata".lower():
            self.search_entry_2.configure(state="disabled")
            number = 0
            self.list_box.delete("all")
            for flight in flights:
                if (flight["flight"]["iata"][0:len(s1)]).lower() == s1:
                    self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
                    number = number + 1

        elif sby == "Icao".lower():
            self.search_entry_2.configure(state="disabled")
            number = 0
            self.list_box.delete("all")
            for flight in flights:
                if (flight["flight"]["icao"][0:len(s1)]).lower() == s1:
                    self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
                    number = number + 1

        elif sby == "Airline".lower():
            self.search_entry_2.configure(state="disabled")
            number = 0
            self.list_box.delete("all")
            for flight in flights:
                if (flight["airline"]["icao"][0:len(s1)]).lower() == s1 or (flight["airline"]["name"][0:len(s1)]).lower() == s1:
                    self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
                    number = number + 1
        elif sby == "Ruote".lower():
            self.search_entry_2.configure(state = "normal")
            number = 0
            if s2 == "":
                self.show_all(flights = flights)
            else:
                self.list_box.delete("all")
                for flight in flights:
                    if (flight["arrival"]["icao"][0:len(s1)]).lower() == s1 and (flight["departure"]["icao"][0:len(s1)]).lower() == s2:
                        self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
                        number = number + 1
            
    def show_all(self,flights):
        number = 0
        self.list_box.delete("all")
        for flight in flights:
            self.list_box.insert(number,f"Number: {flight["flight"]["number"]}\t✈️iata/icoa: {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\t✈️airline: {flight["airline"]["icao"]}")
            number = number + 1

    def get_data(self,Input):
        number = ""
        type2 = self.search_list.get().lower()
        if type2 == "active":
            self.show_map_bt.configure(state = "normal")
        else:
            self.show_map_bt.configure(state = "disabled")

        for i in Input[8:13]:
            if i in ["0","1","2","3","4","5","6","7","8","9"]:
                number += i

        if type2 == "active":
            flights = self.App.flights
        elif type2 == "scheduled":
            flights = self.App.scheduled_flights
        elif type2 == "landed":
            flights = self.App.landed_flights

        for flight in flights:
            if flight["flight"]["number"] == number:
                self.flight_info_label.configure(text = f"[Flight]\n\nFlight Number : {flight["flight"]["number"]}\niata/icoa : {flight["flight"]["iata"]}/{flight["flight"]["icao"]}\nStatus : {flight["flight_status"]}")
                date = self.datetime_changer(flight["departure"]["scheduled"])
                self.departure_info_label.configure(text = f"[departure] \n\nAirport: {flight["departure"]["airport"]}\niata/icoa : {flight["departure"]["iata"]}/{flight["departure"]["icao"]}\nLanding date : {date[0]}\nlanding time : {date[1]}")
                date = self.datetime_changer(flight["arrival"]["scheduled"])
                self.arrival_info_label.configure(text = f"[arrival] \n\nAirport: {flight["arrival"]["airport"]}\niata/icoa : {flight["arrival"]["iata"]}/{flight["arrival"]["icao"]}\nTake off date : {date[0]}\nTake off time : {date[1]}")
                self.airline_info_label.configure(text = f"[Airline] \n\nName : {flight["airline"]["name"]}\niata/icoa : {flight["airline"]["iata"]}/{flight["airline"]["icao"]}")

                lo = self.App.airplane_coordinates(self.App.icao_location(flight["arrival"]["icao"])
                                            ,self.App.icao_location(flight["departure"]["icao"])
                                            ,flight["arrival"]["scheduled"]
                                            ,flight["departure"]["scheduled"]
                                            ,flight["flight_status"])

                self.show_map_bt.configure(command = lambda:self.show_in_map(lo=lo))

    def show_in_map(self,lo):
        self.App.map.set_zoom(13)
        self.App.map.set_position(lo[0][0],lo[0][1])
        
    def datetime_changer(self,datetime_str):
        datetime_object = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
        return datetime_object.date(),datetime_object.time()

if __name__ == "__main__":
    app = Tk()
    my_frame = CTkFrame(app)
    my_frame.pack()
    Search_frame(frame = my_frame)
    app.mainloop()