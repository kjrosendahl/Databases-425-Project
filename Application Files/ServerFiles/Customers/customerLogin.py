def loginVerification(email, pa):
    try: 
        sql = """select CID from OnlineAcc where email = (:email) and password = (:password)"""
        
        # query result 
        cursor.execute(sql, [email, pa])

        x = cursor.fetchall()
        
        # if account exists, return CID
        if x: 
            return (True, x[0][0])
        else: 
            return (False, 'null')
    except DBFailure: 
        print('Something went wrong. Please try again.')
