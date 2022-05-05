# employee: returns a list of inventories
def availableInv(connection) -> list[int]:
    try:
        cursor = connection.cursor()
        sql = """select InvID from Inventory"""
        x = (cursor.execute(sql)).fetchall()
        i = [j[0] for j in x]
        return(i)
    except: 
        return('Something went wrong.')
