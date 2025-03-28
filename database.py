import sqlite3
import os

def resetDatabase():
    if os.path.exists('sign_language.db'):
        os.remove('sign_language.db')
    createDatabase()

###############################################################

def createDatabase():
    conn = sqlite3.connect('sign_language.db')

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS word (
        id INTEGER PRIMARY KEY,
        word TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS frame (
        id INTEGER PRIMARY KEY,
        frame_order INTEGER,
        word_id INTEGER,
        FOREIGN KEY (word_id) REFERENCES word (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag (
        id INTEGER PRIMARY KEY,
        tag_num INTEGER,
        x DOUBLE,
        y DOUBLE,
        z DOUBLE,
        handedness TEXT,
        frame_id INTEGER,
        FOREIGN KEY (frame_id) REFERENCES frame (id)
    )
    ''')

    conn.commit()
    conn.close()

###############################################################

def insertWord(word):
    conn = sqlite3.connect('sign_language.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM word WHERE word = ?
    ''', (word,))

    existing_word = cursor.fetchone()

    if existing_word is None:
        cursor.execute('''
            INSERT INTO word (word) 
            VALUES (?)
        ''', (word,))
        conn.commit()
    else:
        conn.close()
        return False
    conn.close()
    return True

###############################################################

def insertFrame(word, order):
    conn = sqlite3.connect('sign_language.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM word WHERE word = ?
    ''', (word,))
    
    word_id = cursor.fetchone()[0]

    cursor.execute('''
            INSERT INTO frame (frame_order, word_id) 
            VALUES (?, ?)
        ''', (order, word_id))
    
    conn.commit()
    conn.close()

################################################################

def insertTag(word, order, tag_num, handedness, x, y, z):
    conn = sqlite3.connect('sign_language.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT f.id 
        FROM frame f
        JOIN word w ON f.word_id = w.id
        WHERE w.word = ? AND f.frame_order = ?
    ''', (word, order))

    frame_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO tag (tag_num, x, y, z, handedness, frame_id) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tag_num, x, y, z, handedness, frame_id))
    
    conn.commit()
    conn.close()

###############################################################

def GetCoordinatesByWord(word):
    res = []
    conn = sqlite3.connect('sign_language.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT f.id 
        FROM frame f
        JOIN word w ON f.word_id = w.id
        WHERE w.word = ?
    ''', (word,))
    frame_ids = cursor.fetchall()
    for frame_id in frame_ids:
        tmp = []
        cursor.execute('''
            SELECT tag.x, tag.y, tag.z 
            FROM tag
            JOIN frame f ON tag.frame_id = f.id
            WHERE f.id = ? AND tag.handedness = "Left"
        ''', (frame_id[0],))
        coordinates = cursor.fetchall()
        print(str(frame_id[0]) + " Left" + str(len(coordinates)))
        tmp.append(coordinates)
        cursor.execute('''
            SELECT tag.x, tag.y, tag.z 
            FROM tag
            JOIN frame f ON tag.frame_id = f.id
            WHERE f.id = ? AND tag.handedness = "Right"
        ''', (frame_id[0],))
        coordinates = cursor.fetchall()
        print(str(frame_id[0]) + " Right" + str(len(coordinates)))
        tmp.append(coordinates)
        res.append(tmp)
    conn.close()
    return res

# resetDatabase()