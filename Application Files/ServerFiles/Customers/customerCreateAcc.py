# Customer: create account
def createAccount(CID, email, password, street, city, state, zipcode): 
    try: 
        try: 
            sql = """insert into OnlineAcc values (:CID, :email, :password)"""
            cursor.execute(sql, [CID, email, password])
        except:
            print('Something went wrong. Please enter a valid and unique email and password.')

        try: 
            sql = """insert into CustAddress values (:CID, :street, :city, :state, :zipcode)"""
            cursor.execute(sql, [CID, street, city, state, zipcode])
        except:
            print('Something went wrong. Please enter a valid address.')
        
        connection.commit()
        return(True, CID, "Account created successfully.")
    except: 
        return(False, "null", "Something went wrong. Please try again.")
        
