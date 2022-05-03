"""
placing orders through the website 
-- requires that PIDs, Quantities are passed in as a list (for calculating the total, and checking inventory has the stock)

Does the following: 
1) calculates the total 
2) checks that the customer has enough credit to place the order
3) checks the quantities are valid, and that PIDs/InvIDs are valid
4) creates a new record for the order
5) inserts the products of the order into the OrderProd relation 
6) generates the tracking number and randomly chooses a shipping company
7) inserts the shipping information 
8) (through triggers) automatically decreases the inventory quantity accordingly

"""

def placeOrder(CID: int, InvID: int, PIDs: list[int], Quantities: list[int]): 
    items = len(PIDs)
    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    year = dt.year
    status = "Pending" 
    typeOrder = "Online"
    total = 0 
    
    # make sure that quantites, product, inventories are right. Calculate total 
    for i in range(items): 
        PID = PIDs[i]
        q = Quantities[i]
        sql = """select Quantity, Price from ProdInv where InvID = :InvID and PID = :PID"""
        x = (cursor.execute(sql, [InvID, PID])).fetchall()
        if not x: 
            return(False, 'null', 'null', 'Order failed. Wrong Product or Inventory entered.')
        elif x[0][0] < q: 
            return(False, 'null', 'null', "Order failed. Too many products entered.")
        else: 
            total = total + q*(x[0][1])
            
    # decrease credit 
    sql = """select credit from Credit where CID = :CID"""
    x = (cursor.execute(sql, [CID])).fetchall()[0][0]
    if x < total: 
        return(False, 'null', 'null', "Order failed. You do not have enough credit.")
    else: 
        sql = """update Credit set credit = credit - :total where CID = :CID"""
        x = (cursor.execute(sql, [total, CID]))
            
    # create new order record 
    try: 
        sql = """select max(OrderID) from Orders"""
        x = (cursor.execute(sql)).fetchall()
        if x[0][0] is None: 
            OrderID = 1
        else: 
            OrderID = x[0][0] + 1 
        
        sql = """insert into Orders values (:OrderID, :CID, :InvID, :status, :typeOrder, :total, :day, :month, :year)"""
        x = cursor.execute(sql, [OrderID, CID, InvID, status, typeOrder, total, day, month, year])
    except: 
        return(False, 'null', 'null', "Something went wrong. Please try again.")
    
    # insert the products ordered into the OrderProd relation
    for i in range(items): 
        PID = PIDs[i]
        q = Quantities[i]
        sql = """insert into OrderProd values(:OrderID, :PID, :InvID, :quantity)"""
        x = (cursor.execute(sql, [OrderID, PID, InvID, q]))
    
    # generate new tracking number
    sql = """select max(trackNo) from OrderShip"""
    x = (cursor.execute(sql)).fetchall()
    if x[0][0] is None: 
        trackNo = 1
    else: 
        trackNo = x[0][0] + 1
        
    # randomly choose shipping company
    sql = """select * from Shipping"""
    x = (cursor.execute(sql)).fetchall()
    r = random.choice(x)
    ShipID = r[0]
    comp = r[1]
    
    # insert the order shipment details 
    sql = """insert into OrderShip values(:OrderID, :ShipID, :trackNo)"""
    x = (cursor.execute(sql, [OrderID, ShipID, trackNo]))
    
    connection.commit()
    return(True, trackNo, comp, "Order placed.")
