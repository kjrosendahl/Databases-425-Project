"""
manually creates an order that was placed in store, for a customer with NO account or doesn't want to tie it to an accont(employee application)
-- requires PIDs, Quantites are passed in as a list 

Does the following: 
1) calculates the total 
3) checks the quantities are valid, and that PIDs/InvIDs are valid
4) creates a new record for the order
5) inserts the products of the order into the OrderProd relation
8) (through triggers) automatically decreases the inventory quantity accordingly

"""

def inStoreOrderNoAcc(InvID: int, PIDs: list[int], Quantities: list[int]): 
    try:
        items = len(PIDs)
        dt = datetime.datetime.today()
        day = dt.day
        month = dt.month
        year = dt.year
        status = "Complete"
        typeOrder = "In Store"
        total = 0 

        CID = newCustomerRecord('null')[1]

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
