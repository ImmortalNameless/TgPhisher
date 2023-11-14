import sqlite3

class DB:

    path = "./databases/{db_name}.db"

    def __init__(self, db_name: str) -> None:
        self.conn = sqlite3.connect(self.path.format(db_name=db_name))
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        try:
            data = self.cur.execute("SELECT * FROM `users`").fetchone()
        except:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS `users` (
                             `user_id` INT,
                             `first_name` TEXT,
                             `last_name` TEXT,
                             `phone` TEXT
            )''')
            self.conn.commit()
        try:
            data1 = self.cur.execute("SELECT * FROM `refers`").fetchone()
        except:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS `refers` (
                             `user_id` INT,
                             `refer` INT
            )''')
            self.conn.commit()

    def add_user(self, user_id: int|str, f_name="", l_name="", phone="") -> None:
        self.cur.execute("INSERT INTO `users` VALUES (?,?,?,?)", [user_id, f_name, l_name, phone])
        self.conn.commit()

    def add_ref(self, user_id, refer):
        self.cur.execute("INSERT INTO `refers` VALUES (?,?)", [user_id, refer])
        self.conn.commit()

    def is_ref(self, user_id: int|str) -> bool:
        data = self.cur.execute("SELECT * FROM `refers` WHERE `user_id`=?", [user_id,]).fetchone()
        if data == None:
            return False
        else:
            return True

    def get_count(self, user_id):
        data = self.cur.execute("SELECT COUNT(user_id) FROM `refers` WHERE `refer`=?", [user_id,]).fetchone()
        return data[0]
    
    def ger_refs(self, user_id):
        data = self.cur.execute("SELECT user_id FROM refers WHERE refer=?", [user_id, ]).fetchall()
        return data

    def is_exist(self, user_id: int|str) -> bool:
        data = self.cur.execute("SELECT * FROM `users` WHERE `user_id`=?", [user_id,]).fetchone()
        if data == None:
            return False
        else:
            return True
        
    def close(self):
        self.conn.close()