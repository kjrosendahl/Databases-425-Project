# returns a list of InventoryIDs, Name, and Addresses of Stores
def searchStoreInvID(): 
    try: 
        sql = """select InvID, Name, Street, City, State, Zipcode from Inventory natural join Stores natural join Addresses"""
        cursor.execute(sql)
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")

        
