# employee: login verification 
# returns boolean and message, or EID
def loginVerificationEmployee(connection, EID: int, password: str): 
    try: 
        cursor = connection.cursor()
        sql = """select password from Employees where EmpID = :EID"""
        x = (cursor.execute(sql, [EID])).fetchall()
        if x[0][0] != password: 
            return(False, 'Incorrect password')
        else: 
            return(True, EID)
    except: 
        return(False, 'Something went wrong.')
    
