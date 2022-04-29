# customer may request their credit card info. Returns T/F, tuple of card info or null, and message
def requestCredit(CID):
    try: 
        sql = """select * from Credit where CID = :CID"""
        cursor.execute(sql, [CID])
        x = cursor.fetchall()
        
        if(x):
            return(True, x[0], "Card found")
        else: 
            return(False, "null", "Card not found.")
    except: 
        ("Something went wrong. Try again.")
