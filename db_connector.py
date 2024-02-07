import psycopg2

def connect():
    conn = psycopg2.connect(database='chatbot', user='tastepass', password='tastepass', host='127.0.0.1', port='5432')
    return conn.cursor()