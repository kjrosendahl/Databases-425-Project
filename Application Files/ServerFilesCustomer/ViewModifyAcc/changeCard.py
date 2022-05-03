# customers with accounts may change their card info 
# returns boolean, card number or error message 
def changeCard(CID, CardNumber, CVV):
    try: 
        credit = 1000
        
        sql = """update Credit set CardNo = :CardNumber, CVV = :CVV, credit = :credit where CID = :CID"""
        cursor.execute(sql, [CardNumber, CVV, credit, CID])
        
        connection.commit()
        
        return (True, CardNumber)
    except: 
        return(False, "Something went wrong. Enter a valid card number.")
