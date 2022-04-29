# returns a list of the products, product info when given an inventory ID, limit by the category ID
def InvRequestLimCat(ID, CatID):
    try: 
        sql = """select PID, ProductName, Price, Quantity, BrandName, CategoryName from ProdInv natural join 
                Products natural join Brands natural join Categories where InvID = :ID and CategoryID = :CatID"""
        cursor.execute(sql, [ID, CatID])
        x = cursor.fetchall()
        return(x)
    except: 
        ("Something went wrong. Try again.")
