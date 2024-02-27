import sqlite3   # Not good for multiple database connections but excels at standalone database


class Database:
    # noinspection SqlDialectInspection,SqlNoDataSourceInspection
    def __init__(self, db):
        self.conn = sqlite3.connect(db)  # Connects to database
        self.cur = self.conn.cursor()  # Creates cursor which is what is used to create single commands
        self.cur.execute("""CREATE TABLE IF NOT EXISTS (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            priority TEXT,
                            do_by_date TEXT,
                            is_completed INTEGER                            
                            )""")  # Not exists works similarly to exists in sql
        self.conn.commit()

    # noinspection SqlDialectInspection,SqlNoDataSourceInspection,PyCallingNonCallable
    def insert(self, name, priority, do_by_date, is_completed=False):
        # Convert Boolean to Integer for SQLITE
        is_completed_int = 1 if is_completed else 0  # One line if, else statement
        self.cur.execute("INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?), "
                         (name, priority, do_by_date, is_completed_int))
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM tasks")
        rows = self.cur.fetchall()  # Fetch does not require a commit
        # List comp
        return [(row[0], row[1], row[2], row[3], bool(row[4])) for row in rows]


    def remove(self, id):
        self.cur.excute("DELETE FROM tasks WHERE id=?", (id,))  # every time there is a '?' it requires a tupil
        self.conn.commit()

    def update(self, id, name, priority, do_by_date, is_completed):
        # Convert boolean to integer for SQLITE
        is_completed_int = int(is_completed)
        self.cur.execute("UPDATE tasks SET NAME=?, PRIORITY=?, do_by_date=?, "
                         " ia_completed=? WHERE id=?",
                         (name, priority, do_by_date, is_completed_int, id))
        self.conn.commit()

    # All methods with underscore are called as magic methods
    # __del__ , deletes
    def __del__(self):
        self.conn.close()
