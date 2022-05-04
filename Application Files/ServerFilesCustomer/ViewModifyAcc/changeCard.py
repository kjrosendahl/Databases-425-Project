# customers with accounts may change their card info 
# returns boolean, card number or error message 
def changeCard(connection, CID: int, CardNumber: int, CVV: int):
    try:
        cursor = connection.cursor()
        credit = 1000
        
        sql = """update Credit set CardNo = :CardNumber, CVV = :CVV, credit = :credit where CID = :CID"""
        cursor.execute(sql, [CardNumber, CVV, credit, CID])
        
        connection.commit()
        
        return (True, CardNumber)
    except: 
        return(False, "Something went wrong. Enter a valid card number.")
