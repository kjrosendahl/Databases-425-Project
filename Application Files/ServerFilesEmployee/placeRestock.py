"""
placing a restock order through the website (employee application)
-- requires PIDs, Quantites are passed in as a list 

Does the following: 
1) checks that the passkey for updating inventory is correct 
2) checks at all passed in PIDs are made by the passed in manufacturer
3) creates a new record for the restock order 
4) inserts the products of the restock into the RestockProd relation 
5.a) (through triggers) automatically increases the inventory quantity 
5.b) if the product wasn't in the inventory to start, creates a new record for the product in Inventory, then updates  

"""
def placeRestock(InvID: int, PIDs: list[int], Quantities: list[int], ManID: int, passkey: str): 
    items = len(PIDs)
    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    year = dt.year
    status = "Pending"   
    default_q = 0
    default_price = 100
    
    try: 
        sql = """select passkey from Inventory where InvID = :InvID"""
        x = cursor.execute(sql, [InvID]).fetchall()
        if x[0][0] != passkey: 
            return(False, 'null', 'null', 'Order failed. Wrong passkey entered.')


        # make sure that the products are sent to the appropriate manufacturer
        for i in range(items): 
            PID = PIDs[i]
            q = Quantities[i]
            sql = """select * from Manufacturer where ManID = :ManID and PID = :PID"""
            x = (cursor.execute(sql, [ManID, PID])).fetchall()
            if not x: 
                return(False, 'null', 'null', 'Order failed. The manufacturer does not make all entered products.')
            else: 
                if x[0][3] < q: 
                    return(False, 'null', 'null', 'Order failed. The manufacturer does not have enough product quantities.')

        # create new restock order 

        sql = """select max(RestockID) from Restock"""
        x = (cursor.execute(sql)).fetchall()
        if x[0][0] is None: 
            RID = 1
        else: 
            RID = x[0][0] + 1 

        sql = """insert into Restock values (:RID, :InvID, :ManID, :day, :month, :year, :status)"""
        cursor.execute(sql, [RID, InvID, ManID, day, month, year, status])

        # insert the products ordered into restock Prod 
        for i in range(items): 
            PID = PIDs[i]
            q = Quantities[i]

            sql = """select * from ProdInv where PID = :PID and InvID = :InvID"""
            x = cursor.execute(sql, [PID, InvID]).fetchall()

            if not x: 
                sql = """insert into ProdInv values (:InvID, :PID, :quantity, :price)"""
                cursor.execute(sql, [InvID, PID, default_q, default_price])

            sql = """insert into RestockProd values(:RID, :PID, :InvID, :quantity)"""
            cursor.execute(sql, [RID, PID, InvID, q])

        connection.commit()

        return(True, RID, InvID, 'Restock Order placed.')

    except: 
        return(False, 'null', 'null', 'Something went wrong.')
