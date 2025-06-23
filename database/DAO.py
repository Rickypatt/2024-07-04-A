from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.datetime ) as anni
                        from sighting s
                        order by anni desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anni"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.datetime ) as anni
                        from sighting s
                        order by anni desc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_shape(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape
                            from sighting s
                            where year(s.datetime ) = %s
                            and shape is not null
                            and shape != ""
                            order by shape asc"""
            cursor.execute(query,(anno,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_nodes(anno, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from sighting s
                        where year(s.datetime ) = %s
                        and s.shape  = %s"""
            cursor.execute(query, (anno,forma))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges(anno, forma,idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1,s2.id as id2, s1.`datetime` as d1,s2.datetime as d2
                        from sighting s1, sighting s2
                        where year(s1.datetime ) = %s
                        and year(s1.datetime ) = year(s2.datetime )
                        and s1.shape = %s
                        and s1.shape = s2.shape
                        and s1.datetime < s2.datetime
                        and s1.state = s2.state
                        group by s1.id,s2.id"""
            cursor.execute(query, (anno,forma))

            for row in cursor:
                result.append((idMap[row["id1"]], idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result

