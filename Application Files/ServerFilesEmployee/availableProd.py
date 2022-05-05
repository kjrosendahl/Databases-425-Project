# employee: returns a list of all products and their info (PID, brand, category, name)
def availableProd(connection): 
    try:
        cursor = connection.cursor()
        sql = """select * from Products"""
        x = (cursor.execute(sql)).fetchall()
        return(x)
    except:
        return('Something went wrong.')
