import sqlite3

def fetch_herb_effect(c, herb_effect):
    print herb_effect
    herb = "-1"
    for line in c.execute("select idh from herbs where name=?", [herb_effect[0]]):
        herb = line[0]
    effect = "-1"
    for line in c.execute("select ide from effects where name=?", [herb_effect[1]]):
        effect = line[0]
    return herb, effect

def main(data_folder):
    with sqlite3.connect('herbalist.db') as st:
        # Init database
        st.execute("DROP TABLE IF EXISTS herbs")
        st.execute("CREATE TABLE herbs(idh INTEGER PRIMARY KEY, name varchar)")
        st.execute("DROP TABLE IF EXISTS effects")
        st.execute("CREATE TABLE effects(ide INTEGER PRIMARY KEY, name varchar)")
        with open(data_folder+"/herbs.csv") as f:
            for line in f:
                st.execute("INSERT INTO herbs(name) VALUES (?)", [line[:-1]])
        with open(data_folder+"/effects.csv") as f:
            for line in f:
                st.execute("INSERT INTO effects(name) VALUES (?)", [line[:-1]])
        # Create range of possibility
        st.execute("DROP TABLE IF EXISTS unknown")
        st.execute("CREATE TABLE unknown(ide INTEGER, idh INTEGER, PRIMARY KEY (ide, idh))")
        st.execute("INSERT INTO unknown select ide, idh from herbs, effects")

        ## Init found effects
        st.execute("DROP TABLE IF EXISTS known")
        st.execute("CREATE TABLE known(ide INTEGER, idh INTEGER, PRIMARY KEY (ide, idh))")
        with open(data_folder+"/effects_found.csv") as f:
            for line in f:
                st.execute("INSERT INTO known(idh, ide) VALUES (?, ?)", fetch_herb_effect(st, line[:-1].split(",")))

        for line in st.execute("SELECT * from known"):
            print line

main("data_test")