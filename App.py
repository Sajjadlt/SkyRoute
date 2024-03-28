from tkinter import *
from customtkinter import *
from tkintermapview import *
from PIL import Image, ImageTk
import requests
import math
from datetime import datetime, timezone
import time
import decimal
from local_api import Local_api
from tkinter import messagebox
import sqlite3
from geopy.geocoders import Nominatim

from settings_frame import Settings_frame
from search_frame import Search_frame
from ticket_frame import Ticket_frame

api_key = "your api.aviationstack.com API key :)"


class AviationStackAPI():
    def __init__(self, api_key):
        self.base_url = "http://api.aviationstack.com/v1"
        super().__init__()
        self.api_key = api_key

    def get_landed_flights(self):
        url = f"{self.base_url}/flights"
        params = {"flight_status": "landed","access_key" : self.api_key }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            flights = data['data']
            return flights

    def get_scheduled_flights(self):
        url = f"{self.base_url}/flights"
        params = {"flight_status": "scheduled","access_key" : self.api_key }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            flights = data['data']
            return flights

    def get_live_flights(self):
        url = f"{self.base_url}/flights"
        params = {"flight_status": "active","access_key" : self.api_key }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            flights = data['data']
            return flights

    def get_airport_location(self):
        api_url = f"http://api.aviationstack.com/v1/airports?access_key={self.api_key}"
        response = requests.get(api_url)
        data = response.json()["data"]
        list1 = list()
        for airport in data:
            airport_name = airport["airport_name"]
            latitude = airport["latitude"]
            longitude = airport["longitude"]
            x = (airport_name,latitude,longitude)
            list1.append(x)

        return list1

#================================================================================================
#================================================================================================

class App_user():
    def __init__(self,root = Tk):
        self.root = root
        self.root.withdraw()

        self.airports_conn = sqlite3.connect('airports.db')
        self.airports_cursor = self.airports_conn.cursor()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        w_c = self.centerWindow(800,533,self.root)
        self.loading_page = Toplevel()
        self.loading_page.overrideredirect(True)
        self.loading_page.title("Loading...")
        self.loading_page.geometry(f"800x533+{w_c[0]}+{w_c[1]}")
        self.loading_page.resizable(0,0)

        self.loading_image = [PhotoImage(file='images//loading.gif',format = 'gif -index %i' %(i)) for i in range(8)]
        self.loading_lb = Label(self.loading_page)
        self.loading_lb.pack(expand=True, fill=BOTH)
        self.loading_time = 0
        self.loading_percent = 0
        self.loading_page.after(200,self.loading)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.API = AviationStackAPI(api_key=api_key)

        
        self.markers = [i for i in range(200)]
        self.get_api_json()
        self.create_map()
        self.create_main_frame()
        self.create_widgets()
    
        self.load_settings()
        self.show_airplanes()
        self.map.set_position(30,30)
        self.my_time()

    def get_api_json(self):
        #if you dont have API key , you can use local API 
        self.flights = self.API.get_live_flights()
        #self.flights = Local_api.get()
        #self.airports = self.API.get_airport_location()
        self.airports = Local_api.get_airports()
        self.landed_flights = self.API.get_landed_flights()
        #self.landed_flights = Local_api.get_landed_flights()
        self.scheduled_flights = self.API.get_scheduled_flights()
        #self.scheduled_flights = Local_api.get_scheduled()

        self.root.after(3600000,self.get_api_json)
    
    def centerWindow(self,width, height, root):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return int(x), int(y)
        
    def loading(self):
        photo = self.loading_image[self.loading_time]
        self.loading_time += 1
        self.loading_percent += 10
        if self.loading_time == 8:
            self.loading_time = 0

        if self.loading_percent <= 160:
            self.loading_lb.configure(image=photo)
            self.loading_lb.PhotoImage = photo
            self.loading_page.after(200, self.loading)
        else :
            self.root.deiconify()  
            self.loading_page.destroy() 

    def load_settings(self):
        con = sqlite3.connect(database=r'settins.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from settings where row=1")
            row=cur.fetchone()
            new_map = row[2]
            show_airports = row[3]
            con.close()
            if show_airports == "on":
                self.show_airports()
            if new_map == "OpenStreetMap":
                self.map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            elif new_map == "Google normal":
                self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            elif new_map == "Google satellite":
                self.map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent =self.root)

    def show_airports(self):
        try:
            image_open = Image.open("images/airport.png").resize((15, 15))
            airport_icon = ImageTk.PhotoImage(image=image_open)
            for airport in self.airports:
                self.map.set_marker(float(airport[1]),float(airport[2]), text="", icon=airport_icon)
        except:
            pass

    def create_widgets(self):
        self.time_lb = CTkLabel(self.map,font=("",20,"bold"),text_color="#000000",bg_color="transparent")
        self.time_lb.place(x = 1400,y=10)

        icon =ImageTk.PhotoImage(Image.open("images/icon.png"))
        icon_lb = Label(self.root , image=icon)
        icon_lb.place(x=655.5,y = 10)
        icon_lb.PhotoImage = icon

        icon_name =ImageTk.PhotoImage(Image.open("images/icon_name.png"))
        icon_name_lb = Label(self.root , image=icon_name)
        icon_name_lb.place(x=655.5+68,y = 25)
        icon_name_lb.PhotoImage = icon_name

    def my_time(self):
        now = datetime.now(tz=timezone.utc).strftime("%H:%M")
        self.time_lb.configure(text=f"{now} UTC")
        self.time_lb.after(30000,self.my_time)
    
    def airplane_coordinates(self,origin,destination,time1, time2,status):
        if origin == None:
            return None
        elif destination == None:
            return None
        else :
            if status == "scheduled" :
                return origin,angle_degrees
            elif status == "landed":
                return  destination, angle_degrees
            else:
                x1, y1 = origin
                x2, y2  = destination

                angle = math.atan2((y2 - y1), (x2 - x1))
                angle_degrees = math.degrees(angle)
                #======================
                datetime1 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%S+00:00")
                datetime2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%S+00:00")
                delta = datetime2-datetime1
            
                second = abs(delta.total_seconds())

                if delta.total_seconds() < 0:
                    length_oftrip =  -second
                else:
                    length_oftrip = second
                #===========================
                dt = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%S%z")

                now = datetime.now(timezone.utc)

                delta =now-dt 
                
                second = abs(delta.total_seconds())

                past_time_oftravel  = second if abs(delta.total_seconds()) > 0 else -second
                decimal.getcontext().prec = 10

                part = decimal.Decimal(str(past_time_oftravel))  
                whole = decimal.Decimal(str(length_oftrip))

                percentage = (part / whole) /10
                if abs(float(percentage)) >= 1 :
                    return destination,angle_degrees

                x = x1 + ((x2 - x1) * abs(float(percentage)))
                y = y1 + ((x2 - x1) * abs(float(percentage)))
                return (x,y),angle_degrees

    def create_map(self):
        self.map = TkinterMapView(self.root,bg_color="#666666",use_database_only=False)
        self.map.pack(fill=BOTH,expand= True)

        self.map.set_zoom(0)
        self.map.add_right_click_menu_command(label="Copy coordinates",command=self.copy_coord,pass_coords=True)

    def copy_coord(self,x):
        self.root.clipboard_clear()
        self.root.clipboard_append(f"{x[0]} {x[1]}")

    def icao_location(self,icao_code):
        self.airports_cursor.execute("SELECT latitude, longitude FROM airports WHERE icao=? ",(icao_code,))
        row = self.airports_cursor.fetchone()
        if row: 
            return row
        return None
    
        with open("texts/airports.txt", "r", encoding="latin-1") as file:
            for line in file:
                data = line.split(",")
                if data[5].strip('"') == icao_code:
                    latitude = float(data[6])
                    longitude = float(data[7])
                    
                    return latitude, longitude
        return None
    
    def show_airplanes(self):
        a = 0 
        try:
            image_open = Image.open("images/airplane.png").resize((30, 30))
            for i in self.flights:
                x = self.airplane_coordinates(self.icao_location(i["arrival"]["icao"])
                                            ,self.icao_location(i["departure"]["icao"])
                                            ,i["arrival"]["scheduled"]
                                            ,i["departure"]["scheduled"]
                                            ,i["flight_status"])
                if x == None or x == ():
                    continue
                else:
                    plane_image = ImageTk.PhotoImage(image=image_open.rotate(x[1]))
                    marker = self.map.set_marker(x[0][0],x[0][1], text="", icon=plane_image)
                    self.markers.append(marker)
                    self.delete_marker(marker=self.markers[a])
                    a += 1
        except Exception:
            pass
       
        self.main_frame.after(1000,self.show_airplanes)

    def delete_marker(self,marker):
        self.map.delete(marker)
        self.markers.pop(0)

    def create_main_frame(self):
        mainframe_im =ImageTk.PhotoImage(Image.open("images/frame_lb.png").resize((500,100)))
        self.main_frame = Label(self.root,image=mainframe_im,text="")
        self.main_frame.place( x = 518, y = 650)
        self.main_frame.PhotoImage = mainframe_im

        settings_icon =ImageTk.PhotoImage(Image.open("images/settings.png").resize((80,80), Image.LANCZOS))
        settings_bt = Button(self.main_frame,command=self.create_settings_frame,bg="#333333",fg="#333333",image=settings_icon ,text="",border=0,activebackground="#333333",activeforeground="#333333")
        settings_bt.place(x = 36 , y = 10)
        settings_bt.PhotoImage = settings_icon
      
        search_icon =ImageTk.PhotoImage(Image.open("images/search.png").resize((80,80), Image.LANCZOS))
        search_bt = Button(self.main_frame,command=self.create_search_frame,bg="#333333",fg="#333333",image=search_icon ,text="",border=0,activebackground="#333333",activeforeground="#333333")
        search_bt.place(x = 113+36 , y = 10)
        search_bt.PhotoImage = search_icon

        search_icon =ImageTk.PhotoImage(Image.open("images/loction.png").resize((80,80), Image.LANCZOS))
        search_bt = Button(self.main_frame,command=self.user_location,bg="#333333",fg="#333333",image=search_icon ,text="",border=0,activebackground="#333333",activeforeground="#333333")
        search_bt.place(x = 113+36+80+36 , y = 10)
        search_bt.PhotoImage = search_icon

        search_icon =ImageTk.PhotoImage(Image.open("images/ticket.png").resize((80,80), Image.LANCZOS))
        search_bt = Button(self.main_frame,command=self.create_ticket_frame,bg="#333333",fg="#333333",image=search_icon ,text="",border=0,activebackground="#333333",activeforeground="#333333")
        search_bt.place(x = 113+36+80+36+80+36 , y = 10)
        search_bt.PhotoImage = search_icon

    def user_location(self):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode("address")
        x = (location.latitude, location.longitude)
        self.map.set_marker(x[0],x[1])

    def create_ticket_frame(self):
        my_frame = CTkFrame(self.root,width=100,height=100)
        my_frame.place(x = 268 , y =80)
        Ticket_frame(my_frame,App=self)

    def create_settings_frame(self):
        my_frame = CTkFrame(self.root,width=100,height=100)
        my_frame.place(x = 418 , y =150)
        Settings_frame(my_frame,App=self)

    def create_search_frame(self):
        my_frame = CTkFrame(self.root,width=100,height=100)
        my_frame.place(x = 268 , y =80)
        Search_frame(my_frame,App=self)

if __name__ == "__main__":
    app = Tk(className=" SkyRoute")
    app.geometry("1536x800+0+0")
    #app.state('zoomed')
    #app.resizable(0,0)
    App_user(app)
    app.mainloop()
