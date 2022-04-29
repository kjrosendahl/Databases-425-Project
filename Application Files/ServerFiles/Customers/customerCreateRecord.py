# Customer: create a new record
def newCustomerRecord(Name): 
    try: 
        sql = """select max(CID) from Customer"""
        cursor.execute(sql)  
        x = cursor.fetchall()
        CID = x[0][0] + 1
        
        sql = """insert into Customer values (:CID, :Name, :Frequent)"""
        cursor.execute(sql, [CID, Name, "False"])
        
        connection.commit()
        return(True, CID)
    except:
        return(False, "null")