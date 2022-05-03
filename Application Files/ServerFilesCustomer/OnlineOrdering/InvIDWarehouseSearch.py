# returns a list of InventoryIDs and Addresses of Warehouses
def searchWareInvID(): 
    try: 
        sql = """select InvID, Street, City, State, Zipcode, Region from Inventory natural join Warehouses natural join Addresses"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
