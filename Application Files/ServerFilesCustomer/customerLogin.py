def loginVerification(connection, email: str, pa: str):
    try:
        cursor = connection.cursor()
        sql = """select CID from OnlineAcc where email = (:email) and password = (:password)"""
        
        # query result 
        cursor.execute(sql, [email, pa])

        x = cursor.fetchall()
        
        # if account exists, return CID
        if x: 
            return (True, x[0][0], "Account verified")
        else: 
            return (False, None, "Login information incorrect")
    except DBFailure: 
        print('Something went wrong. Please try again.')
