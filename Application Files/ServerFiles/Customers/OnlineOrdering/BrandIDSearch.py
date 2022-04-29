# returns a list of brandIDs and their name
def searchBrandID():
    try: 
        sql = """select * from Brands"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
