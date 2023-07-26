import sqlite3 as sl

"""
SELECT ('столбцы или * для выбора всех столбцов; обязательно')
FROM ('таблица; обязательно')
WHERE ('условие/фильтрация, например, city = 'Moscow'; необязательно')
GROUP BY ('столбец, по которому хотим сгруппировать данные; необязательно')
HAVING ('условие/фильтрация на уровне сгруппированных данных; необязательно')
ORDER BY ('столбец, по которому хотим отсортировать вывод; необязательно')
"""

con = sl.connect('help_teh.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        phone_number TEXT, 
        adress TEXT, 
        telegram_id,
        UNIQUE (phone_number)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Programs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            settings TEXT,
            instructions TEXT
        
            
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Admins (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                position TEXT,
                name TEXT
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Comment (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                comment TEXT,
                programs_id INTEGER,
                clients_id TEXT,
                accept BOOLEAN,
                FOREIGN KEY (client_id) REFERENCES Clients (id),
                FOREIGN KEY (programs_id) REFERENCES Programs (id)
        );
                    
    """)


with con:
    data = con.execute("SELECT * FROM Clients")
    print(data.fetchall())
    # fetchone