# customers may delete their account 
# deletes their Account, card info, and address
# returns boolean, message
def deleteAcc(CID: int): 
    try: 
        sql = """delete from OnlineAcc where CID = :CID"""
        cursor.execute(sql, [CID])
        sql = """delete from Credit where CID = :CID"""
        cursor.execute(sql, [CID])
        sql = """delete from CustAddress where CID = :CID"""
        cursor.execute(sql, [CID])
        
        connection.commit()
        
        return (True, 'Account deleted.')
    except: 
        return(False, 'Something went wrong. Please try again.')
