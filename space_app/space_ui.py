#user interface for application
from tkinter import *
import tkMessageBox
import tkFont
from PIL import ImageTk,Image
import locate
import numpy as np
import astropy.io.fits as fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astroquery.jplhorizons import conf,Horizons
conf.horizons_server = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi'
from tkinter import ttk
import pdb
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import math
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import  axes3d,Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from weather import Weather, Unit


window = Tk()
def update_clock():
    now = time.strftime("%H:%M:%S")
    label3.configure(text=now)
    window.after(1000, update_clock)

def update_weather():
	weather = Weather(Unit.FAHRENHEIT)
	lookup = weather.lookup_by_latlng(38.5449,-121.7405)
	condition = lookup.condition
	condtxt = condition.text
	windtxt = lookup.wind.speed	
	temptxt = lookup.condition.temp
	label4.configure(text="Current Conditions:  "+condtxt, font = "Times 15 bold")
	label5.configure(text="Temperature:  "+temptxt+ " F", font = "Times 15 bold")
	label6.configure(text="Windspeed:  "+windtxt + "  mph", font = "Times 15 bold")


weather = Weather(Unit.FAHRENHEIT)
lookup = weather.lookup_by_latlng(38.5449,-121.7405)
condition = lookup.condition
condtxt = condition.text
windtxt = lookup.wind.speed
temptxt = lookup.condition.temp

data  = np.array([])
now = datetime.datetime.now()
x = now.strftime("%Y-%m-%d %H:%M:%S")
# adding background image

background_image= PhotoImage(file = '/home/aakash/Pictures/death_star.png')
background_label = Label(window, image= background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# generic labels
label1 = Label(window, text = "2A$ JPL Horizons Query Portal", font = "Times 20 bold")
label1.grid(row = 0, column = 0)

label2 = Label(window, text = "Object ID", font = "Times 15 bold")
label2.grid(row = 1, column = 1)

label3 = Label(window, text = x, font = "Times 15 bold")
label3.grid(row = 2, column = 4)

label4 = Label(window, text = "Current Conditions:  "+condtxt, font = "Times 15 bold")
label4.grid(row = 3, column = 0)

label5 = Label(window, text = "Temperature:  "+temptxt+ " F", font = "Times 15 bold")
label5.grid(row = 4, column = 0)

label6 = Label(window, text = "Windspeed:  "+windtxt + "  mph", font = "Times 15 bold")
label6.grid(row = 5, column = 0)

# entries
title_text = StringVar()
e1 = Entry(window)
e1.grid(row = 1, column = 2)


# insert datatable

tree = ttk.Treeview(window, columns = (1,2), height = 5, show = "headings")

tree.heading(1, text="Azi")
tree.heading(2, text="Elevation")


scroll = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scroll.grid(row = 5, column = 3)
tree.configure(yscrollcommand=scroll.set)
tree.grid(row = 5, column = 2)

#enable button

def callback1():
	update_clock()
	update_weather()
	for i in tree.get_children():
		tree.delete(i)
	redraw(0,0)

b = Button(window, text="RESET", bg = "yellow" ,command=callback1)
b.grid(row =3 , column = 4)

def callback2():
	window.quit()
	window.destroy()

b = Button(window, text="QUIT", bg = "red",command=callback2)
b.grid(row =7 , column = 0)

def redraw(angle, angle2):
	x,y,z = 0,0,0
	endy = 2*math.sin(math.radians(angle))
	endx = 2*math.cos(math.radians(angle))
	endz = 2*math.tan(math.radians(angle2))

	fig = Figure(figsize=(4, 4), dpi=100)
	fig.add_subplot(111, projection='3d').set_ylim([-10, 10]) 
	fig.add_subplot(111, projection='3d').set_zlim([-10, 10])  # set the bounds to be 10, 10
	fig.add_subplot(111, projection='3d').set_xlim([-10, 10])
	fig.add_subplot(111, projection='3d').plot([x, endx], [y, endy], [z,endz])
	canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
	canvas.draw()
	canvas.get_tk_widget().grid(row = 6, column = 0)
	fig.add_subplot(111, projection='3d').mouse_init()
	fig.add_subplot(111, projection='3d').plot([x, endx], [y, endy], [z,endz])

def callback():
    data = locate.locate(e1.get())
    angle = data[0]
    angle2 = data[1]
    for val in data:
    	tree.insert('', 'end', values = data)
    redraw(angle, angle2)

b = Button(window, text="ENABLE", bg = "green"  ,command=callback)
b.grid(row =1 , column = 0)

update_clock()
window.mainloop()