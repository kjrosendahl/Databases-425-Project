# returns a list of brandIDs and their name
def searchBrandID(connection):
    try:
        cursor = connection.cursor()
        sql = """select * from Brands"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
