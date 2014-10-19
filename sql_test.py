import sqlite3

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
        # init unknown effects for each herb
        st.execute("DROP TABLE IF EXISTS unknown")
        st.execute("CREATE TABLE unknown(ide INTEGER, idh INTEGER, PRIMARY KEY (ide, idh))")
        st.execute("INSERT INTO unknown select ide, idh from herbs, effects")

        ## Init known effects
        st.execute("DROP TABLE IF EXISTS known")
        st.execute("CREATE TABLE known(ide INTEGER, idh INTEGER, PRIMARY KEY (ide, idh))")
        # with open(data_folder+"/effects_found.csv") as f:
        #     for line in f:
        #         st.execute("INSERT INTO known(idh, ide) VALUES (?, ?)", fetch_herb_effect(st, line[:-1].split(",")))


        ## Load mix history
        st.execute("DROP TABLE IF EXISTS mix")
        st.execute("CREATE TABLE mix(idm INTEGER PRIMARY KEY, failed boolean)")
        st.execute("DROP TABLE IF EXISTS mix_herbs")
        st.execute("CREATE TABLE mix_herbs(idm INTEGER, idh INTEGER,failed boolean, PRIMARY KEY(idm,idh))")
        with open(data_folder+"/mix.csv") as f:
            for line in f:
                failed = False
                herbs_effects = line[:-1].split(";")
                for effect in herbs_effects[1].split(","):
                    if effect == "-1":
                        failed = True
                idmix = st.execute("INSERT INTO mix values(null, ?)", [failed]).lastrowid
                for herb in herbs_effects[0].split(","):
                    st.execute("INSERT INTO mix_herbs(idm, idh) " +
                               "VALUES (?,(select idh from herbs where name=?))", [idmix, herb])
                    for effect in herbs_effects[1].split(","):
                        if effect != "-1":
                            st.execute("INSERT INTO known(idh, ide) VALUES ((select idh from herbs where name=?),"
                                       " (select ide from effects where name=?))", [herb, effect])
        removed = 1
        while removed !=0:
            removed = 0
            ## Remove unknown effects using known effects
            res = st.execute("DELETE FROM unknown WHERE ide IN (select known.ide from known where known.idh = unknown.idh)")
            removed += res.rowcount
            ## Remove unknown effects when known effects is equal to max effect by herb
            res = st.execute("DELETE FROM unknown WHERE idh IN (SELECT idh from known k group by idh having count(ide) = 3)")
            removed += res.rowcount
            ## Remove unknown effects of B using failed mix of herb A and B where A.effect is known
            res = st.execute("DELETE FROM unknown WHERE ide IN "
                       "(SELECT known.ide FROM known, mix_herbs WHERE known.idh = mix_herbs.idh AND mix_herbs.idm IN"
                       "(SELECT mix.idm FROM mix,mix_herbs mh WHERE mix.failed AND mix.idm = mh.idm"
                       " AND mh.idh = unknown.idh))")
            removed += res.rowcount
            ##Add known effects if unknown effects is reduced to max effect by herb
            res = st.execute("insert into known SELECT uk.ide,uk.idh from unknown uk where uk.idh IN (SELECT herbs.idh from herbs"
                       " WHERE 3 - (select count(*) from known k where k.idh = herbs.idh) - (select count(*) "
                       "from unknown u where u.idh = herbs.idh) = 0)")
            removed += res.rowcount
            print "Remove unknown "+str(removed)




        print "Known"
        for line in st.execute("SELECT h.name, e.name from known u, herbs h, effects e "
                               "where u.idh = h.idh and u.ide=e.ide order by h.name, e.name"):
            print line[0], line[1]
        print "Unknown"
        for line in st.execute("SELECT h.name, e.name from unknown u, herbs h, effects e "
                               "where u.idh = h.idh and u.ide=e.ide order by h.name, e.name"):
            print line[0], line[1]
main("data_test")