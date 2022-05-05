# Customer: enter credit card 
def createCreditCard(connection, CID: int, CardNo: int): 
    try:
        cursor = connection.cursor()
        try: 
            credit = 1000
            sql = """insert into Credit values (:CID, :CardNo, :credit)"""
            cursor.execute(sql, [CID, CardNo, credit])
            
            connection.commit()
            return(True, CID, "Card added successfully.")
        except Exception as E: 
            print("Card Failed", E)
            return(False, CID, "Card unsuccessful. Please enter a valid and unique credit card information.")
    except: 
        return(False, CID, "Something went wrong. Please try again.")
