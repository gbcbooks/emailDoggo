import sqlite3


class DataStore:
    def __init__(self, db_file='web_crawler.db'):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls (url TEXT PRIMARY KEY, content TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails (email TEXT PRIMARY KEY, url TEXT)''')
        conn.commit()
        conn.close()

    def insert_url(self, url, content):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            query = "INSERT INTO urls (url, content) VALUES (?, ?)"
            cursor.execute(query, (url, content))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"URL {url} already exists in the database.")
        conn.close()

    def insert_emails(self, emails, url):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for email in emails:
            try:
                query = "INSERT INTO emails (email, url) VALUES (?, ?)"
                cursor.execute(query, (email, url))
                conn.commit()
                print(f"Inserted email {email} from URL {url} into the database.")
            except sqlite3.IntegrityError:
                print(f"Email {email} already exists in the database.")
        conn.close()
