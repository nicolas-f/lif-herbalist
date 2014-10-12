import sqlite3
with sqlite3.connect('herbalist.db') as st:
    st.execute("DROP TABLE IF EXISTS herbs")
    st.execute("CREATE TABLE herbs(idh INTEGER PRIMARY KEY, name varchar)")
    with open("data/herbs.csv") as f:
        for line in f:
            st.execute("INSERT INTO HERBS(name) VALUES (?)", [line[:-1]])
    for row in st.execute("SELECT * from herbs"):
        print row