import psycopg2
import scrape_data
import pandas as pd
import time
import os


def connect_to_db():
    DATABASE_URL = os.environ["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn


def create_tables(conn):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS sssbdata (address VARCHAR(255), dagar INTEGER[], url VARCHAR(255), type VARCHAR(255))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS sssbdata_closed (address VARCHAR(255), dagar INTEGER[], url VARCHAR(255), type VARCHAR(255))"
    )
    cur.close()


def fetch_all_rows(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM sssbdata")
    rows = cur.fetchall()
    cur.close()
    return rows


def update_row(conn, address, days):
    cur = conn.cursor()
    cur.execute(f"UPDATE sssbdata SET dagar =ARRAY{days} WHERE address = '{address}'")
    conn.commit()
    cur.close()


def delete_row(conn, address):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM sssbdata WHERE address = '{address}'")
    conn.commit()
    cur.close()


def insert_row(conn, address, days, url, _type):
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO sssbdata (address, dagar, url, type) VALUES ('{address}', ARRAY[{days}], '{url}', '{_type}')"
    )
    conn.commit()
    cur.close()


def append_closed(conn, row):
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO sssbdata_closed (address, dagar, url, type) VALUES ('{row[0]}', ARRAY{row[1]}, '{row[2]}', '{row[3]}')"
    )
    conn.commit()
    cur.close()


def compare_and_save(df):
    timer = time.time()
    print("Saving")
    conn = connect_to_db()
    create_tables(conn)
    rows = fetch_all_rows(conn)

    for row in rows:
        address = row[0]
        days = row[1]
        if address not in df["address"].unique():
            append_closed(conn, row)
            delete_row(conn, address)
        else:
            last_day = df[df["address"] == address]["dagar"].values[0]
            if days is None or days == []:
                days = [last_day]
            elif last_day != days[-1]:
                days.append(last_day)
                days = [
                    day
                    for i, day in enumerate(days)
                    if day != 0 and (i + 1 >= len(days) or day + 1 != days[i + 1])
                ]
            update_row(conn, address, days)

    for address in df["address"].unique():
        if address not in [row[0] for row in rows]:
            insert_row(
                conn,
                address,
                df[df["address"] == address]["dagar"].values[0],
                df[df["address"] == address]["url"].values[0],
                df[df["address"] == address]["type"].values[0],
            )
            print("Added new row")

    conn.close()
    print(f"Saved in {time.time() - timer} seconds")


if __name__ == "__main__":
    df = scrape_data.scrape()
    compare_and_save(df)
