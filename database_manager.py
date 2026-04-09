import sqlite3

class DatabaseManager:
    def __init__(self, db_name="chess.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    # 🔹 TABLE SETUP
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result TEXT DEFAULT 'ongoing'
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Move (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            move_number INTEGER,
            from_square TEXT,
            to_square TEXT,
            piece TEXT
        )
        """)

        self.conn.commit()

    # 🔹 CORE METHODS (ADD THEM HERE 👇)

    def create_game(self):
        self.cursor.execute("INSERT INTO Game (result) VALUES ('ongoing')")
        self.conn.commit()
        return self.cursor.lastrowid

    def save_move(self, game_id, move_number, from_sq, to_sq, piece):
        self.cursor.execute("""
        INSERT INTO Move (game_id, move_number, from_square, to_square, piece)
        VALUES (?, ?, ?, ?, ?)
        """, (game_id, move_number, from_sq, to_sq, piece))
        self.conn.commit()

    def end_game(self, game_id, result):
        self.cursor.execute(
            "UPDATE Game SET result=? WHERE id=?",
            (result, game_id)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()