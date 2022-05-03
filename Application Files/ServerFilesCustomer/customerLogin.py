def loginVerification(email: str, pa: str):
    try: 
        sql = """select CID from OnlineAcc where email = (:email) and password = (:password)"""
        
        # query result 
        cursor.execute(sql, [email, pa])

        x = cursor.fetchall()
        
        # if account exists, return CID
        if x: 
            return (True, x[0][0])
        else: 
            return (False, None)
    except DBFailure: 
        print('Something went wrong. Please try again.')
