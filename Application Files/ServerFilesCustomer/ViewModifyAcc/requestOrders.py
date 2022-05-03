# frequent customers may request their previous orders. Rereturns a list of tuples of the broad order details 
def requestOrders(email): 
    sql = """select OrderID, day, month, year, total, status, typeOrder from Orders natural join OnlineAcc 
            where email = :email"""
    x = (cursor.execute(sql, [email])).fetchall()
    return(x)
