# frequent customers may request their previous orders. Rereturns a list of tuples of the broad order details 
def requestOrders(connection, email: str): 
    cursor = connection.cursor()    
    sql = """select OrderID, Odate, total, status from Orders natural join OnlineAcc  where email = :email"""
    x = (cursor.execute(sql, [email])).fetchall()
    return(x)
