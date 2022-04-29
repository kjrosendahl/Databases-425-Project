# returns a list of the products, product info when given an inventory ID, limit by the brand ID
def InvRequestLimBrand(ID, BID):
    try: 
        sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                Products natural join Brands natural join Categories where InvID = :ID and BrandID = :BID"""
        cursor.execute(sql, [ID, BID])
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
