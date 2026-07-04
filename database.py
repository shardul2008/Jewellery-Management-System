import sqlite3

conn = sqlite3.connect("jewellery.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jewellery(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    metal TEXT,
    purity TEXT,
    weight REAL,
    making REAL,
    gst REAL,
    other REAL,
    final_price REAL   
)
""")

conn.commit()


def add_jewellery(name, metal, purity, weight, making, gst, other,final_price ):
    cursor.execute("""
    INSERT INTO jewellery
    (name, metal, purity, weight, making, gst, other,final_price )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, metal, purity, weight, making, gst, other, final_price))
    conn.commit()


def view_jewellery():
    cursor.execute("SELECT * FROM jewellery")
    return cursor.fetchall()


def update_jewellery(id, name, metal, purity, weight, making, gst, other, final_price):
    cursor.execute("""
    UPDATE jewellery
    SET
        name=?,
        metal=?,
        purity=?,
        weight=?,
        making=?,
        gst=?,
        other=?,
        final_price=?
        
    WHERE id=?
    """,(name, metal, purity, weight, making, gst, other,final_price, id))

    conn.commit()


def delete_jewellery(id):
    cursor.execute("DELETE FROM jewellery WHERE id =?",(id,))
    conn.commit()


def search_jewellery(name):
    cursor.execute(
        "SELECT * FROM jewellery WHERE name LIKE ?",
        ('%' + name + '%',)
    )
    return cursor.fetchall()


def get_jewellery_by_id(id):
    cursor.execute(
        "SELECT * FROM jewellery WHERE id = ?",(id,)
    )
    return cursor.fetchone()
