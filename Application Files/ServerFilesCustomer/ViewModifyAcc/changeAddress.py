# customers with accounts may change their address info 
# returns boolean, address or error message 
def changeAddress(CID, Street, City, State, Zipcode): 
    try: 
        sql = """update CustAddress set Street = :Street, City = :City, State = :State, Zipcode = :Zipcode where CID = :CID"""
        cursor.execute(sql, [Street, City, State, Zipcode, CID])
        
        connection.commit()
        
        return(True, (Street, City, State, Zipcode))
    except: 
        return(False, 'Something went wrong. Enter a valid address.')
