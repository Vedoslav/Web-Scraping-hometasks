import sqlite3
def read_sql() -> None:
    filename = 'C:/Users/User/Documents/rdWS/quotes.db'

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    
    sql = """SELECT * FROM quotes where author == 'Albert Einstein' """
    rows = cursor.execute(sql).fetchall()
    print(rows)
    
    connection.close()

if __name__ == '__main__':
    read_sql()
