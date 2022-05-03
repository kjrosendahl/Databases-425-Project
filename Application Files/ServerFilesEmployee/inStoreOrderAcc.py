"""
manually creates an order that was placed in store, for a customer with an account (employee application)
-- requires PIDs, Quantites are passed in as a list 

Does the following: 
1) calculates the total 
2) checks that the customer has an account, and enough credit
3) checks the quantities are valid, and that PIDs/InvIDs are valid
4) creates a new record for the order
5) inserts the products of the order into the OrderProd relation
8) (through triggers) automatically decreases the inventory quantity accordingly

"""
def inStoreOrderAcc(email: str, InvID: int, PIDs: list[int], Quantities: list[int]): 
    try:
        items = len(PIDs)
        dt = datetime.datetime.today()
        day = dt.day
        month = dt.month
        year = dt.year
        status = "Complete"
        typeOrder = "In Store"
        total = 0 

        sql = """select CID from OnlineAcc where email = :email"""
        x = cursor.execute(sql, [email]).fetchall()
        if not x: 
            return(False, 'null', 'null', 'Order failed. There is no account registered to this email.')
        else: 
            CID = x[0][0]

        # make sure that quantites, products, inventories are right. Calculate total 
        for i in range(items): 
            PID = PIDs[i]
            q = Quantities[i]
            sql = """select Quantity, Price from ProdInv where InvID = :InvID and PID = :PID"""
            x = (cursor.execute(sql, [InvID, PID])).fetchall()
            if not x: 
                return(False, 'null', 'null', 'Order failed. Wrong Product or Inventory entered.')
            elif x[0][0] < q: 
                return(False, 'null', "Order failed. Too many products entered.")
            else: 
                total = total + q*(x[0][1])

        # decrease credit 
        sql = """select credit from Credit where CID = :CID"""
        x = (cursor.execute(sql, [CID])).fetchall()[0][0]
        if x < total: 
            return(False, 'null', "Order failed. You do not have enough credit.")
        else: 
            sql = """update Credit set credit = credit - :total where CID = :CID"""
            cursor.execute(sql, [total, CID])

        # create new order record 
        sql = """select max(OrderID) from Orders"""
        x = (cursor.execute(sql)).fetchall()
        if x[0][0] is None: 
            OrderID = 1
        else: 
            OrderID = x[0][0] + 1 

        sql = """insert into Orders values (:OrderID, :CID, :InvID, :status, :typeOrder, :total, :day, :month, :year)"""
        x = cursor.execute(sql, [OrderID, CID, InvID, status, typeOrder, total, day, month, year])

        # insert the products ordered into the OrderProd relation
        for i in range(items): 
            PID = PIDs[i]
            q = Quantities[i]
            sql = """insert into OrderProd values(:OrderID, :PID, :InvID, :quantity)"""
            x = (cursor.execute(sql, [OrderID, PID, InvID, q]))

        connection.commit()

        return(True, OrderID, 'Order placed.')
    except: 
        return(False, 'null', 'Something went wrong.')
