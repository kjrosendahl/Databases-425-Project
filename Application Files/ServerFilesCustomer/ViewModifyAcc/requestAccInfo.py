# customers may request info about their account 
# returns list of the form: [(CID, Name, email), (Card Number, CVV, Credit), (Street, City, State, ZipCode), [orders]
# orders: list of tuples of orders (see request Orders)
# if any of this (account info, card info, address info) isn't in database, returns error message instead of tuple
from ServerFilesCustomer.PaymentPage.requestCredit import requestCredit
from ServerFilesCustomer.ViewModifyAcc.requestOrders import requestOrders
from ServerFilesCustomer.PaymentPage.requestAddress import requestAddress

def requestAccInfo(connection, CID: int): 
    cursor = connection.cursor()
    sql = """select CID, Name, email from OnlineAcc natural join Customer where CID = :CID"""
    x = (cursor.execute(sql, [CID])).fetchall()
    if not x: 
        info = "Account not found."
    else:
        info = x[0]
    y = requestCredit(CID)
    if not y[0]:
        credit = "Card not found."
    else: 
        credit = y[1][1:]
    z = requestAddress(CID)
    if not z[0]: 
        address = "Address not found."
    else: 
        address = z[1][1:]
    a = requestOrders(info[2])
    if not a: 
        orders = "Orders not found."
    else:
        orders = a
    return[info, credit, address, orders]
