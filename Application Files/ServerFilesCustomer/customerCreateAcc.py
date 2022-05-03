# Customer: create account (requires Customer ID, email/password)
def createAccount(CID: int, email: str, password: str):
    try: 
        try: 
            sql = """insert into OnlineAcc values (:CID, :email, :password)"""
            cursor.execute(sql, [CID, email, password])
            
            connection.commit()
            return(True, CID, "Account created successfully.")
            
        except: 
            return(False, CID, "Account unsuccessful. Please enter a unique email. Passwords must be at least 6 characters.")
        
    except: 
        return(False, "null", "Something went wrong. Please try again.")
        
