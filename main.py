from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import pstats
import psutil
from PIL import Image, ImageTk

import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

from time import strftime

from tkcalendar import *

import pyautogui

import subprocess
import webbrowser as wb
import random

root = Tk()
root.title("SuperMegaGyperAPP")
root.geometry("850x500+300+170")
root.resizable(False,False)
root.configure(bg="#000000")   #292e29

image_icon = PhotoImage(file="images/debuging.png")
root.iconphoto(False,image_icon)

Body = Frame(root,width=900, height=600, bg="#000000")   #d6d6d6
Body.pack(pady=20,padx=20)

System_Frame = Frame(Body,width=310,heigh=310, bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1) #435
System_Frame.place(x=10,y=10)

laptop_image = Image.open("images/laptop.png")
laptop_image = laptop_image.resize((200,200))
photo = ImageTk.PhotoImage(laptop_image)
myimage = Label(System_Frame, image=photo, background="#f4f5f5")
myimage.place(x=50, y=20)

my_system = platform.uname()

l1 = Label(System_Frame, text=my_system.node, bg="#f4f5f5", font=("Times new roman", 10, 'bold'))
l1.place(x=60, y=200)

l2 = Label(System_Frame, text=f'System:{my_system.system}', bg="#f4f5f5", font=("Times new roman", 10, 'bold'))
l2.place(x=60, y=220)

l3 = Label(System_Frame, text=f'Machine:{my_system.machine}', bg="#f4f5f5", font=("Times new roman", 10, 'bold'))
l3.place(x=60, y=240)

#---------------------------------------------------------------------------------------------------------------------#

V_and_B_Frame = Frame(Body,width=310,heigh=115, bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
V_and_B_Frame.place(x=10,y=330)

Volume_label = Label(V_and_B_Frame,text="Volume:", font=("Times new Roman", 10, "bold"), bg="#f4f5f5")
Volume_label.place(x=60,y=30)
volume_value = tk.DoubleVar()

def get_current_volume_value():
    return '{: .2f}'.format(volume_value.get())

def volume_changed(event):
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER((IAudioEndpointVolume)))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()), None)

style = ttk.Style()
style.configure("TScale", background="#f4f5f5")
volume = ttk.Scale(V_and_B_Frame, from_=60, to=0, orient="horizontal", command=volume_changed, variable=volume_value)

volume.place(x=170,y=30)

Bright_label = Label(V_and_B_Frame, text="Sonne:",font=("Times new Roman", 10, "bold"), bg="#f4f5f5")
Bright_label.place(x=60,y=65)

brightness_value = tk.DoubleVar()

def get_current_brightnes():
    return '{: .2f}'.format((brightness_value.get()))

def bright_change(event):
    sbc.set_brightness(get_current_brightnes())

brightness = ttk.Scale(V_and_B_Frame, from_=0, to=100, orient='horizontal', command=bright_change, variable=brightness_value)
brightness.place(x=170, y=65)

#---------------------------------------------------------------------------------------------------------------------#

State_Frame = Frame(Body,width=230,heigh=230, bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
State_Frame.place(x=330,y=10)

system = Label(State_Frame, text="System", font=("Robotic", 10), bg="#f4f5f5")
system.place(x=90,y=10)

def time_converter(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours,minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def charge_detector():
    global battery_image
    global battery_png
    global bl_in_BL
    battery = psutil.sensors_battery()
    percent = battery.percent
    time = time_converter(battery.secsleft)


    Battery_label.config(text=f"{percent}%")
    Battery_label_plug.config(text=f"Plug in: {str(battery.power_plugged)}")
    if not battery.power_plugged:
        Battery_label_time.config(text=f"{time} remaining")

    bl_in_BL = Label(State_Frame, background="#f4f5f5")
    bl_in_BL.place(x=15,y=40)

    Battery_label.after(1000, charge_detector)

    if battery.power_plugged == True:
        if percent<=50:
            battery_png = Image.open("images/butter_plugged_less.png")
            battery_png = battery_png.resize((90, 90))
            battery_image = ImageTk.PhotoImage(battery_png)
            bl_in_BL.config(image=battery_image)
        if percent>50:
            battery_png = Image.open("images/battery_plugged_full.png")
            battery_png = battery_png.resize((90, 90))
            battery_image = ImageTk.PhotoImage(battery_png)
            bl_in_BL.config(image=battery_image, background="#f4f5f5")
    else:
        if percent<=20:
            battery_png = Image.open("images/battery_low.png")
            battery_png = battery_png.resize((90, 90))
            battery_image = ImageTk.PhotoImage(battery_png)
            bl_in_BL.config(image=battery_image)
        if percent>20:
            battery_png = Image.open("images/battery_full.png")
            battery_png = battery_png.resize((90, 90))
            battery_image = ImageTk.PhotoImage(battery_png)
            bl_in_BL.config(image=battery_image)

Battery_label = Label(State_Frame, font=("Robotic", 20, "bold"), bg="#f4f5f5")
Battery_label.place(x=130,y=70)

Battery_label_plug = Label(State_Frame, font=("Robotic", 10), bg="#f4f5f5")
Battery_label_plug.place(x=20,y=140)

Battery_label_time = Label(State_Frame, font=("Robotic", 10), bg="#f4f5f5")
Battery_label_time.place(x=20,y=165)

charge_detector()

#---------------------------------------------------------------------------------------------------------------------#

Some_Frame = Frame(Body,width=230,heigh=230, bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
Some_Frame.place(x=570,y=10)

text_label = Label(Some_Frame, text="Lets talk about \n what time is it?", font=("arial", 15, "bold"), bg="#f4f5f5")
text_label.place(x=10,y=10)

def clock():
    text = strftime("%H:%M:%S")
    lable_1.config(text=text)
    lable_1.after(1000, clock)

lable_1 = Label(Some_Frame, font=("digital-7", 30,"bold"),bg="#f4f5f5")
lable_1.place(x=10, y=80)
clock()

#---------------------------------------------------------------------------------------------------------------------#

App_Frame = Frame(Body, width=470, heigh=190, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
App_Frame.place(x=330, y=255)

app_label = Label(App_Frame, text="Apps", font=("Robotic", 10), bg="#f4f5f5")
app_label.place(x=210, y=1)

def weather():
    weather_button=Toplevel()
    weather_button.geometry("850x500+300+170")
    weather_button.title('Weather')
    weather_button.configure(bg="#f4f5f5")
    weather_button.resizable(False, False)

    weather_icon = PhotoImage(file="images/weather.png")
    weather_button.iconphoto(False, weather_icon)

    def getWeather():
        try:
            city = Search_field.get()
            geolocator = Nominatim(user_agent="geoapiExpress")
            location = geolocator.geocode(city)
            data = TimezoneFinder()
            result = data.timezone_at(lng=location.longitude, lat=location.latitude)

            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M:%p")
            name.config(text="CURRENT WEATHER", font=("arial", 20, "bold"))
            clock.config(text=current_time, font=("arial", 15, "bold"))

            api = "https://api.openweathermap.org/data/2.5/weather?q=" + city +"&appid=646824f2b7b86caffec1d0b16ea77f79"

            json_data = requests.get(api).json()
            print(json_data)
            condition = json_data["weather"][0]["main"]
            description = json_data["weather"][0]['description']
            temperature = int(json_data["main"]["temp"]-273)
            presure = json_data["main"]["pressure"]
            humidity = json_data["main"]["humidity"]
            wind = json_data["wind"]["speed"]

            t.config(text=(f"{temperature}°, {condition}"))
            c.config(text=(f" FEELS LIKE {temperature}°"))

            Wind.config(text=wind)
            Humidity.config(text=humidity)
            Description.config(text=description)
            Pressure.config(text=presure)
            important_label.config(text=f"time in {city}:")

        except Exception as e:
            pass

    search_image = Image.open("images/search.png")
    search_image = search_image.resize((400,50))
    search_image = ImageTk.PhotoImage(search_image)
    Image_lable = Label(weather_button,image=search_image, bg='#f4f5f5')
    Image_lable.place(x=10,y=15)

    Search_field = tk.Entry(weather_button, justify="center", width=20, font=('Robotic', 15, "bold"), bg="#4f6664", border=0, fg='white')
    Search_field.place(x=50,y=30)
    Search_field.focus()

    search_icon = Image.open("images/search_icon.png")
    search_icon = search_icon.resize((30,30))
    search_icon = ImageTk.PhotoImage(search_icon)
    Search_button = Button(weather_button, image=search_icon, borderwidth=0, cursor="hand2", bg="#4f6664", command = getWeather)
    Search_button.place(x=370, y=26)

    Frame_image = Image.open("images/rectangle.png")
    Frame_image = Frame_image.resize((800,200))
    Frame_image = ImageTk.PhotoImage(Frame_image)
    location_label = Label(weather_button, image=Frame_image, bg="#f4f5f5")
    location_label.pack(padx=5, pady=5, side=BOTTOM)

    important_label = Label(weather_button, font=("arial", 20, "bold"), bg="#f4f5f5", fg="#1b8f7c")
    important_label.place(x=420,y=80)

    name = Label(weather_button, font=("arial", 10), bg="#f4f5f5")
    name.place(x=30,y=80)
    clock = Label(weather_button, font=("Times new Roman", 15), bg="#f4f5f5")
    clock.place(x=420,y=140)

    label_1 = Label(weather_button, text="WIND", font=("Times new roman", 10, "bold"), fg="white", bg="#1e1e20")
    label_1.place(x=100, y=330)

    label_2 = Label(weather_button, text="HUMIDITY", font=("Times new roman", 10, "bold"), fg="white", bg="#1e1e20")
    label_2.place(x=270, y=330)

    label_3 = Label(weather_button, text="DESCRIPTION", font=("Times new roman", 10, "bold"), fg="white", bg="#1e1e20")
    label_3.place(x=450, y=330)

    label_4 = Label(weather_button, text="PRESSURE", font=("Times new roman", 10, "bold"), fg="white", bg="#1e1e20")
    label_4.place(x=670, y=330)

    t = Label(weather_button, font=("arial", 30, "bold"), fg="#ee666d", bg="#f4f5f5")
    t.place(x=30, y=120)
    c = Label(weather_button,font=("arial", 30, "bold"),fg="#06155c", bg="#f4f5f5")
    c.place(x=30, y=170)

    Wind = Label(weather_button, text="---", font=("arial", 15, "bold"), fg="#ffffff", bg="#1e1e20")
    Wind.place(x=100, y=350)
    Humidity = Label(weather_button, text="---", font=("arial", 15, "bold"), fg="#ffffff", bg="#1e1e20")
    Humidity.place(x=280, y=350)
    Description = Label(weather_button, text="---", font=("arial", 15, "bold"), fg="#ffffff", bg="#1e1e20")
    Description.place(x=450, y=350)
    Pressure = Label(weather_button, text="---", font=("arial", 15, "bold"), fg="#ffffff", bg="#1e1e20")
    Pressure.place(x=670, y=350)

    weather_button.mainloop()

def calendar():
    calendar_button = Toplevel()
    calendar_button.geometry("300x300")
    calendar_button.title('Calendar')
    calendar_button.configure(bg="#f4f5f5")
    calendar_button.resizable(False, False)

    calendar_icon = PhotoImage(file="images/calendar.png")
    calendar_button.iconphoto(False, calendar_icon)

    calendar = Calendar(calendar_button, selectmode='day',date_pattern='d/m/yy')
    calendar.pack(padx=15,pady=35)

    calendar_button.mainloop()

def youtube_redirector():
    pass

youtube_png = Image.open("images/youtube.png")
youtube_png = youtube_png.resize((100,80))
youtube_png = ImageTk.PhotoImage(youtube_png)
youtube_button = Button(App_Frame,image=youtube_png,bd=0, command=youtube_redirector)
youtube_button.place(x=60, y=70)

weather_png = Image.open("images/weather.png")
weather_png = weather_png.resize((100,80))
weather_png = ImageTk.PhotoImage(weather_png)
weather_button = Button(App_Frame,image=weather_png,bd=0, command = weather)
weather_button.place(x=175, y=70)

calendar_png = Image.open("images/calendar.png")
calendar_png = calendar_png.resize((100,80))
calendar_png = ImageTk.PhotoImage(calendar_png)
calendar_button = Button(App_Frame,image=calendar_png,bd=0, command=calendar)
calendar_button.place(x=285, y=70)

root.mainloop()