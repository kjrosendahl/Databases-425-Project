# employee: returns a list of manufacturer info (ManID, PID they make, Name of manufacturer, capacity)
def manInfo(connection): 
    try:
        cursor = connection.cursor()
        sql = """select * from Manufacturer"""
        x = (cursor.execute(sql)).fetchall()
        return(x)
    except: 
        return('Someting went wrong.')
