
from tkinter import * 
from customtkinter import *
from tkintermapview import *
from tkinter import messagebox
import sqlite3

class Settings_frame():
    def __init__(self,frame,App = None):
        self.App = App
        frame.configure( width=700,height=400,border_width = 5,border_color = "#008ae6",bg_color= "#000000")

        CTkButton(frame ,command=lambda : frame.destroy(), text="x",font=("",30,"bold"),hover_color = "#2B2B2B",fg_color="#2B2B2B",bg_color = "#2B2B2B",width=20,text_color="#ffffff").place(x=660,y =5)

        CTkLabel(frame , text="Map type :",font=("",15)).place(x=30,y =20)

        self.map_type = CTkOptionMenu(frame, values=["OpenStreetMap", "Google normal", "Google satellite"],command=self.change_map)
        self.map_type.place(x=120,y =20)

        CTkLabel(frame , text="Show airports :",font=("",15)).place(x=30,y =70)

        self.Show_airports = StringVar()
        CTkCheckBox(frame,font=("",15,"bold"), text="", command=self.show_airports,variable=self.Show_airports, onvalue="on", offvalue="off").place(x=150,y =72)

        CTkButton(frame ,command=lambda : App.root.destroy(), text="Exit",font=("",20,"bold"),height=40 ,hover_color = "#ff3333",fg_color="#b30000",bg_color = "#2B2B2B",width=100,text_color="#d9d9d9").place(x=580,y =340)
        CTkButton(frame ,command=lambda : self.save_settings(), text="Save Settings",font=("",18,"bold"),height=40 ,hover_color = "#00cc44",fg_color="#009933",bg_color = "#2B2B2B",width=100,text_color="#0d0d0d").place(x=420,y =340)
        CTkLabel(frame , text="If you don't save the settings\n the changes will be lost by opening the app again!",font=("",12),text_color="#666666").place(x=130,y =350)

        self.load_data()

    def show_airports(self):
        on_or_off = self.Show_airports.get().lower()
        if on_or_off == "on":
            self.App.show_airports()
        elif on_or_off == "off":
            self.App.map.delete_all_marker()
            
    def load_data(self):
        con = sqlite3.connect(database=r'settins.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from settings where row=1")
            row=cur.fetchone()
            new_map = row[2]
            show_airports = row[3]
            con.close()
            self.Show_airports.set(show_airports)
            self.map_type.set(new_map)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent = self.App.root)

    def save_settings(self):
            con = sqlite3.connect(database=r'settins.db')
            cur = con.cursor()
            try:
                cur.execute("Update settings set map_type=?,show_airports=? WHERE row=1",(self.map_type.get(),self.Show_airports.get(),))
                con.commit()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent =self.App.root)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.App.map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.App.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.App.map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

if __name__ == "__main__":
    app = Tk()
    my_frame = CTkFrame(app)
    my_frame.pack()
    Settings_frame(frame = my_frame)
    app.mainloop()