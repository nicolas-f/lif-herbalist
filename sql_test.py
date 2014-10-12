import sqlite3
with sqlite3.connect('herbalist.db') as st:
    # Init database
    st.execute("DROP TABLE IF EXISTS herbs")
    st.execute("CREATE TABLE herbs(idh INTEGER PRIMARY KEY, name varchar)")
    st.execute("DROP TABLE IF EXISTS effects")
    st.execute("CREATE TABLE effects(ide INTEGER PRIMARY KEY, name varchar)")
    with open("data/herbs.csv") as f:
        for line in f:
            st.execute("INSERT INTO herbs(name) VALUES (?)", [line[:-1]])
    with open("data/effects.csv") as f:
        for line in f:
            st.execute("INSERT INTO effects(name) VALUES (?)", [line[:-1]])
    # Create range of possibility
    st.execute("DROP TABLE IF EXISTS potential")
    st.execute("CREATE TABLE potential(ide INTEGER, idh INTEGER, PRIMARY KEY (ide, idh))")
    st.execute("INSERT INTO potential select ide, idh from herbs, effects")
    for line in st.execute("SELECT COUNT(*) from potential"):
        print line