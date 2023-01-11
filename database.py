import sqlite3

con = sqlite3.connect("messages.db")
cur = con.cursor(); #create cursor to be able to search
# check if table exists if not create it 
def message_db():
        
    listOfTables = cur.execute(
    """SELECT name FROM sqlite_master WHERE type='table' AND
    name in ('messages', 'default_messages');""").fetchall()

    if listOfTables == []:
        print('Table not found!')
        cur.execute("""
            create table messages (
            msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message text not null,
            color text not null,
            username text not null,
            status text default 'unread',
            type text default 'text',
            DateInserted DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cur.execute("""
        create table default_messages (
            msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message text not null,
            color text not null,
            type text default 'text'
        );
        """)

        cur.execute("""
            insert into default_messages (message, color)
            values ( '🔴 Live now at twitch.tv/sfmoe', '#FFFFFF'),
                ( '🟢 Starting now... hang on and say hello in chat', '#FFFFFF'),
                ( '🛑 until the next time...find me @sfmoe on most social media', '#c0ffc0');
        """)
        con.commit()
    else:
        print('Table found!')

    default_messages = cur.execute("""
    SELECT * from default_messages
    """).fetchall()

    message_queue = cur.execute("""
    SELECT * FROM messages WHERE status='unread'
    """).fetchall()

    return( (message_queue, default_messages))