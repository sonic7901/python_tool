import psycopg2


def read_issue():
    conn = psycopg2.connect(
        host="odg-cyber-dev-pg11.postgres.database.azure.com",
        database="odg-cymetrics-dev",
        user="cyber@odg-cyber-dev-pg11",
        password="onedegree",
        port=5432
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM issue")
    rows = cur.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    read_issue()
