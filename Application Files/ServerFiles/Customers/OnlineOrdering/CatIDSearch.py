# returns a list of CategoryIDs and their name
def searchCatID():
    try: 
        sql = """select * from Categories"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
