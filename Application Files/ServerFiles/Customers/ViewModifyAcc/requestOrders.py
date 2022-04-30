# frequent customers may request their previous orders. Returns a list of tuples of the broad order details
def requestOrders(email): 
    sql = """select OrderID, day, month, year, total, trackNo, Status from Orders natural join OnlineAcc 
            natural join OrderShip where email = :email"""
    x = (cursor.execute(sql, [email])).fetchall()
    return (x)
