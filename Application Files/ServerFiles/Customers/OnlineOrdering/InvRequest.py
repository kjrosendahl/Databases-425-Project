# returns a list of the products, product info when given an inventory ID
def InvRequest(ID): 
    try: 
        sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                Products natural join Brands natural join Categories where InvID = :ID"""
        cursor.execute(sql, [ID])
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
