# frequent customers may view specific details for a previous order
# requires email and orderID
# checks to see if orderID is valid or if they have the authorization 
# returns either a list of tuples in the form (PID, ProductName, Quantity, Price), or the appropriate error message 
def requestOrderDetails(email, OID): 
    sql = """select CID from Orders where OrderID = :OID"""
    x = (cursor.execute(sql, [OID])).fetchall()
    if not x: 
        return('There are no orders with this ID. Try again.')
    else: 
        check_1 = x[0][0]
    
    sql = """select CID from OnlineAcc where email = :email"""
    x = (cursor.execute(sql, [email])).fetchall()
    if not x: 
        return('There are no orders with this email. Try again.')
    else:
        check_2 = x[0][0]
    
    if check_1 != check_2: 
         return('You are not authorized to view this order.')
    else: 
        sql = """with helper(InvID, PID, ProductName, Quantity) as
                    (select InvID, PID, ProductName, Quantity
                    from Orders natural join OrderProd natural join Products
                    where OrderID = :OID)
                select helper.PID as P_ID, helper.ProductName as PrName, helper.Quantity as quant, price
                from helper left outer join ProdInv on helper.InvID = ProdInv.InvID and helper.PID = ProdInv.PID"""
        x = (cursor.execute(sql, [OID])).fetchall()
        return(x)
        
