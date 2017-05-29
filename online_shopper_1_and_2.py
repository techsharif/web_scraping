# -----Description-----------------------------------------#
#
#  Online Shopper
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for aggregating product data published by a variety of
#  online shops.  See the instruction sheet accompanying this file
#  for full details.
#
# --------------------------------------------------------------------#



# -----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution.)
import os
from urllib import urlopen
import urllib2
# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from Tkinter import *
import tkMessageBox

# Functions for finding all occurrences of a pattern
# defined via a regular expression.  (You do NOT need to
# use these functions in your solution, although you will find
# it difficult to produce a robust solution without using
# regular expressions.)
from re import findall, finditer

# Import the standard SQLite functions just in case they're
# needed.
import sqlite3


#
# --------------------------------------------------------------------#



# -----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the invoice file. To simplify marking, your program should
# produce its results using this file name.
# file_name = 'invoice.html'


# functions for different purpose

def content_between_string(string, start, end):
    data = []
    start_pos = 0
    while (1):
        start_pos = string.find(start, start_pos)
        if start_pos == -1:
            break
        start_pos += len(start)
        end_pos = string.find(end, start_pos)
        if end_pos == -1:
            break

        data += [string[start_pos:end_pos]]
    return data


def just_get_digits(st):
    s = ""
    for i in st:
        if i.isdigit() or i == '.':
            s += i
    return s


def generate_html(data, total):
    str_top = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .main {
            width: 1000px;
            margin: 0 auto;
            padding: 10px;
        }

        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
    </style>
</head>
<body>
<div class="main">
    <h2>Online Shopping</h2>
    <table>
    <tr>
        <th>Image</th>
        <th>Description</th>
        <th>Price</th>
    </tr>'''
    s = ""
    for d in data:
        s += "<tr>"
        s += '<td><img src="' + d['image'] + '"></td>'
        s += '<td>' + d['title'] + '</td>'
        s += '<td>$' + d['price'] + '</td>'
        s += "</tr>"
    s += "<tr>"
    s += '<td></td>'
    s += '<td>Total</td>'
    s += '<td>$' + str(total) + '</td>'
    s += "</tr>"

    str_btm = '''
        </table>
</div>
</body>
</html>
    '''

    file = open('invoice.html', 'w')
    file.write(str_top + s + str_btm)
    file.close()


def get_digital_cameras(numbers):
    response = urllib2.urlopen('http://www.shopzilla.com/digital-cameras/402/products')
    html = str(response.read())
    # print str(html)
    data = content_between_string(html, '<table class="offer result">', '</table>')
    digital_cameras = []
    for d in data:
        try:
            image = content_between_string(d, 'width="75" height="75" src="', '"')[0].replace('&amp;', '&')
            title = content_between_string(d, 'title="', '"')[0]
            price = content_between_string(d, '$', '.')[0]
            digital_cameras += [{
                'title': title,
                'image': image,
                'price': price
            }]
        except:
            print 'error in' + d
    return digital_cameras[-numbers:]


def get_ssds(numbers):
    response = urllib2.urlopen(
        'https://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=636&N=100011693%20600488413%20601193225%20601193224%204814&IsNodeId=1&IsPowerSearch=1&cm_sp=CAT_SSD_2-_-VisNav-_-M.2_1')
    html = str(response.read())
    data = content_between_string(html, 'class="item-container', '"price-save"')
    ssds = []
    for d in data:
        try:
            image = 'http://' + content_between_string(d, 'src="//', '"')[0]
            title = content_between_string(d, 'title="', '"')[0]
            price = content_between_string(d, '</span>$<strong>', '</strong>')[0]
            ssds += [{
                'title': title,
                'image': image,
                'price': price
            }]
        except:
            print 'error in' + d

    return ssds[-numbers:]


def get_phones(numbers):
    response = urllib2.urlopen('https://www.kogan.com/au/shop/phones/')
    html = str(response.read())
    data = content_between_string(html, 'class="product-item"', '</article>')
    phones = []
    for d in data:
        try:
            image = content_between_string(d, 'src="', '"')[0]
            title = content_between_string(d, 'title="', '"')[0]
            price = content_between_string(d, '$', '<')[0]
            phones += [{
                'title': title,
                'image': image,
                'price': price
            }]
        except:
            print 'error in' + d

    return phones[-numbers:]


def store_data(data):
    try:
        # remove all data
        os.remove('shopping_trolley.db')
    except OSError:
        pass
    conn = sqlite3.connect('shopping_trolley.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE purchases
                 (description text, price text)''')

    for d in data:
        # Insert a row of data
        c.execute("INSERT INTO purchases VALUES ('" + d['title'] + "','" + d['price'] + "')")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def calculate_data():
    # get the amount of all data
    ssd = 0 if not e1.get().isdigit() else int(e1.get())
    phone = 0 if not e2.get().isdigit() else int(e2.get())
    dcamera = 0 if not e3.get().isdigit() else int(e3.get())
    # get ssd items
    ssd_items = get_ssds(ssd) if ssd else []
    # get phone items
    phone_items = get_phones(phone) if phone else []
    # get digital camera items
    dcamera_items = get_digital_cameras(dcamera) if dcamera else []
    # variables for count
    sp = pp = dp = 0

    # calculate total price
    for ssd_item in ssd_items:
        ssd_item['price'] = just_get_digits(ssd_item['price'])
        sp += float(ssd_item['price'])
    for phone_item in phone_items:
        phone_item['price'] = just_get_digits(phone_item['price'])
        pp += float(phone_item['price'])
    for dcamera_item in dcamera_items:
        dcamera_item['price'] = just_get_digits(dcamera_item['price'])
        dp += float(dcamera_item['price'])

    # generate html
    generate_html(ssd_items + phone_items + dcamera_items, str(sp + pp + dp))
    result = tkMessageBox.askquestion("Total Price",
                                      'Total Price :$' + str(sp + pp + dp) + "\n Do you want to store it?")
    if result == 'yes':
        store_data(ssd_items + phone_items + dcamera_items)
        tkMessageBox.showinfo('Data saved',"Please see invoice.html for details \nand\nshow shopping_trolley.db to find stored data ")


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
