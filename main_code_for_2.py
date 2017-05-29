import string
from Tkinter import *
import tkMessageBox

from database import store_data
from digital_cameras import get_digital_cameras
from phones import get_phones
from ssd import get_ssds
from test import generate_html, just_get_digits


def calculate_data():
    # process_level.config(text='Start Calculation')
    print "ok"
    ssd = 0 if not e1.get().isdigit() else int(e1.get())
    phone = 0 if not e2.get().isdigit() else int(e2.get())
    dcamera = 0 if not e3.get().isdigit() else int(e3.get())
    print "ok"
    # process_level.config(text='Getting SSD Data')
    ssd_items = get_ssds(ssd) if ssd else []
    print "ok ssd"
    # process_level.config(text='Getting Phone Data')
    phone_items = get_phones(phone) if phone else []
    print "ok phone"
    # process_level.config(text='Getting Camera Data')
    dcamera_items = get_digital_cameras(dcamera) if dcamera else []
    print "ok camera"
    # process_level.config(text='Price Calculating')
    print "ok"
    sp = 0
    pp = 0
    dp = 0

    for ssd_item in ssd_items:
        ssd_item['price'] = just_get_digits(ssd_item['price'])
        sp += float(ssd_item['price'])
    for phone_item in phone_items:
        phone_item['price'] = just_get_digits(phone_item['price'])
        pp += float(phone_item['price'])
    for dcamera_item in dcamera_items:
        dcamera_item['price'] = just_get_digits(dcamera_item['price'])
        dp += float(dcamera_item['price'])
    # process_level.config(text='Total Price :' + str(sp+pp+dp))
    print "ok"
    print("file write")
    generate_html(ssd_items + phone_items + dcamera_items, str(sp + pp + dp))
    result = tkMessageBox.askquestion("Total Price", 'Total Price :$' + str(sp + pp + dp)+"\n Do you want to store it?")
    if result == 'yes':
        store_data(ssd_items + phone_items + dcamera_items)
        print "Data stored"
    else:
        print "Data not stored"


master = Tk()
master.title = 'Online Shop'
Label(master, text="Welcome To").grid(row=0)
Label(master, text="Online shop").grid(row=0, column=1)
Label(master, text="-------------------").grid(row=1, column=0)
Label(master, text="--------------------").grid(row=1, column=1)
Label(master, text=" ").grid(row=2)

Label(master, text="SSD").grid(row=3)
Label(master, text="Phone accessories").grid(row=4)
Label(master, text="Digital Cameras").grid(row=5)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=3, column=1)
e2.grid(row=4, column=1)
e3.grid(row=5, column=1)

process_level = Label(master, text="").grid(row=7)
Button(master, text='Shop', command=calculate_data).grid(row=6, column=1, sticky=W, pady=4)
# Button(master, text='Quit', command=master.quit).grid(row=8, column=1, sticky=W, pady=4)


mainloop()
