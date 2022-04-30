# Customer: enter credit card 
def createCreditCard(CID, CardNo, CVV): 
    try: 
        try: 
            credit = 1000
            sql = """insert into Credit values (:CID, :CardNo, :CVV, :credit)"""
            cursor.execute(sql, [CID, CardNo, CVV, credit])
            
            connection.commit()
            return(True, CID, "Card added successfully.")
        except: 
            return(False, CID, "Card unsuccessful. Please enter a valid and unique credit card information.")
    except: 
        return(False, CID, "Something went wrong. Please try again.")