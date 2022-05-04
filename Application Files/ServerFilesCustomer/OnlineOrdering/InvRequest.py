# returns a list of the products, product info when given an inventory ID. May limit by brandID and catID, otherwise, enter null.
def InvRequest(connection, ID, brandID, catID): 
    try:
        cursor = connection.cursor()
        if not catID and not brandID: 
            sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                    Products natural join Brands natural join Categories where InvID = :ID"""
            cursor.execute(sql, [ID])
        elif not catID and brandID: 
            sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                    Products natural join Brands natural join Categories where InvID = :ID and brandID = :brandID"""
            cursor.execute(sql, [ID, brandID])
        elif not brandID and catID: 
            sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                    Products natural join Brands natural join Categories where InvID = :ID and categoryID = :catID"""
            cursor.execute(sql, [ID, catID])
        else: 
            sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                    Products natural join Brands natural join Categories where InvID = :ID and categoryID = :catID and 
                    brandID = :brandID"""
            cursor.execute(sql, [ID, catID, brandID])
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
