# customer may request their address info. Returns T/F, tuple of info or null, message
def requestAddress(CID: int):
    try: 
        sql = """select * from CustAddress where CID = :CID"""
        cursor.execute(sql, [CID])
        x = cursor.fetchall()
        
        if(x):
            return(True, x[0], "Address found")
        else: 
            return(False, "null", "Address not found.")
    except: 
        ("Something went wrong. Try again.")
