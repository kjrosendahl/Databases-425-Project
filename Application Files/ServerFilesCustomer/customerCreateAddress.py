# Customer: enter address
def createAddress(connection, CID: int, street: str, city: str, state: str, zipcode: int): 
    try: 
        cursor = connection.cursor()
        try:
            sql = """insert into CustAddress values (:CID, :street, :city, :state, :zipcode)"""
            cursor.execute(sql, [CID, street, city, state, zipcode])
            
            connection.commit()
            return(True, CID, "Address added successfully.")
        except Exception as E: 
            print("Address Failed", E)
            return(False, CID, "Address unsuccessful. Please enter a valid address.")
    except: 
        return(False, CID, "Something went wrong. Please try again.")
