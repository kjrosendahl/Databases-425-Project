# customers may change password 
# returns boolean, message 
# only fulfills request if old password is entered correctly 
def changePassword(connection, CID: int, oldPass: str, newPass: str): 
    try:
        cursor = connection.cursor()
        sql = """select Password from OnlineAcc where CID = :CID"""
        x = (cursor.execute(sql, [CID])).fetchall()
        if x[0][0] != oldPass: 
            return(False, 'Please enter the correct current password.')
        else: 
            sql = """update OnlineAcc set Password = :newPass where CID = :CID"""
            cursor.execute(sql, [newPass, CID])

            connection.commit() 

            return(True, 'Password updated.')
    except: 
        return(False, 'Something went wrong. Please enter a valid password.')
