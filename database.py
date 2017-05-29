import sqlite3
import os

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
        c.execute("INSERT INTO purchases VALUES ('"+d['title']+"','"+d['price']+"')")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
