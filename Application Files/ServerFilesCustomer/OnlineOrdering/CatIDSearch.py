# returns a list of CategoryIDs and their name
def searchCatID(connection):
    try:
        cursor = connection.cursor()
        sql = """select * from Categories"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
