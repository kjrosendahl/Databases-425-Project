from http.server import HTTPServer, BaseHTTPRequestHandler
from types import CoroutineType
from urllib.parse import parse_qs, urlparse
import json
import io
import cx_Oracle

HOST = "localhost"
PORT = 9999

# Change your info. Idk how we should do this other than just changing it every time. Don't tell anyone my password though, super secret
CONNECTION = cx_Oracle.connect(
    user="noah",
    password="noah",
    dsn="localhost/xepdb1"
)

def handlePOST(pathStr: str, params: dict, outStream: io.BufferedIOBase):
    match pathStr:
        case "/customer/createCustomer":
            print("Creating new Customer")
            if "name" in params.keys():
                print("Creating Customer")
                from ServerFilesCustomer.customerCreateRecord import newCustomerRecord
                acc = newCustomerRecord(CONNECTION, params["name"])
                print(acc)
                ret = {
                    "success": acc[0],
                    "CID": acc[1]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/verifyLogin":
            print("Veriftying login information")
            if "email" in params.keys() and "password" in params.keys():
                from ServerFilesCustomer.customerLogin import loginVerification
                acc = loginVerification(CONNECTION, params["email"], params["password"])
                ret = {
                    "success": acc[0],
                    "CID": acc[1],
                    "message": acc[2]
                }
                if acc[0]:
                    print("Login Success")
                else:
                    print("Login Failure")
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False, "message": "Incorrect number of arguments"})))

        case "/customer/createAccount":
            print("Creating Online Account")
            # First check if we have the correct data
            if "CID" in params.keys() and "email" in params.keys() and "password" in params.keys() and "cardNumber" in params.keys() and "street" in params.keys() and "city" in params.keys() and "state" in params.keys() and "zipcode" in params.keys():
                
                # First create the onlineAcc
                from ServerFilesCustomer.customerCreateAcc import createAccount
                acc = createAccount(CONNECTION, params["CID"], params["email"], params["password"])
                print(acc)

                # Add the credit card
                from ServerFilesCustomer.customerCreateCard import createCreditCard
                card = createCreditCard(CONNECTION, params["CID"], params["cardNumber"])
                print(card)
                
                # Add the address
                from ServerFilesCustomer.customerCreateAddress import createAddress
                addr = createAddress(CONNECTION, params["CID"], params["street"], params["city"], params["state"], params["zipcode"])
                print(addr)
                if (not acc[0] or not card[0] or not addr[0]):
                    from ServerFilesCustomer.ViewModifyAcc.deleteAcc import deleteAcc
                    suc = deleteAcc(CONNECTION, params["CID"])
                    if not suc[0]:
                        print("Something went wrong trying to delete")

                ret = {
                    "success": acc[0],
                    "message": acc[2],
                    "CID": acc[1]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))
        
        case "/customer/addCreditCard":
            print("Adding Credit Card")
            if "CID" in params.keys() and "cardNumber" in params.keys() and "CVV" in params.keys():
                from ServerFilesCustomer.customerCreateCard import createCreditCard
                card = createCreditCard(CONNECTION, params["CID"], params["cardNumber"], params["CVV"])
                print(card)
                ret = {
                    "success": addr[0],
                    "CID": addr[1],
                    "message": addr
                }
                outStream.write(str.encode(json.dumps(ret)))
        
        case "/customer/addAddress":
            print("Adding Address")
            if "CID" in params.keys() and "street" in params.keys() and "city" in params.keys() and "state" in params.keys() and "zipcode" in params.keys():
                from ServerFilesCustomer.customerCreateAddress import createAddress
                addr = createAddress(CONNECTION, params["CID"], params["street"], params["city"], params["state"], params["zipcode"])
                print(addr)
                ret = {
                    "success": addr[0],
                    "CID": addr[1],
                    "message": addr[2]
                }
                outStream.write(str.encode(json.dumps(ret)))

        case "/customer/orderOnlinePR":
            print("Customer OrderOnline Page Request")
            # First take care of invIds and Names
            from ServerFilesCustomer.OnlineOrdering.InvIDStoreSearch import searchStoreInvID
            inv = searchStoreInvID(CONNECTION)
            invStuff = []
            for i in inv:
                invStuff.append(i[0:2])
            from ServerFilesCustomer.OnlineOrdering.InvIDWarehouseSearch import searchWareInvID
            inv = searchWareInvID(CONNECTION)
            for i in inv:
                invStuff.append([i[0], "Warehouse" + i[0]])

            # Take care of brands
            from ServerFilesCustomer.OnlineOrdering.BrandIDSearch import searchBrandID
            brands = searchBrandID(CONNECTION)

            # Take care of categories
            from ServerFilesCustomer.OnlineOrdering.CatIDSearch import searchCatID
            cats = searchCatID(CONNECTION)

            ret = {
                "success": True,
                "inv": invStuff,
                "brand": brands,
                "cats": cats
            }
            outStream.write(str.encode(json.dumps(ret)))

        case "/customer/orderOnlineInvSearch":
            print("Searching through inventory")
            if "invID" in params.keys():
                catID = params["catID"] if ("catID" in params.keys()) else False
                brandID = params["brandID"] if ("brandID" in params.keys()) else False
                from ServerFilesCustomer.OnlineOrdering.InvRequest import InvRequest
                search = InvRequest(CONNECTION, int(params["invID"]), brandID, catID)
                ret = []
                for i in search:
                    t = {
                        "PID": i[0],
                        "name": i[1],
                        "price": i[2],
                        "quant": i[3],
                        "brandName": i[4],
                        "catName": i[5]
                    }
                    ret.append(t)
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/customerPaymentPR":
            print("Customer Payment Page Request")
            if "CID" in params.keys():
                from ServerFilesCustomer.PaymentPage.requestCredit import requestCredit
                credit = requestCredit(CONNECTION, params["CID"])

                from ServerFilesCustomer.PaymentPage.requestAddress import requestAddress
                addr = requestAddress(CONNECTION, params["CID"])

                if (not credit[0] or not addr[0]):
                    outStream.write(str.encode(json.dumps({"success": False, "message": "No credit card and address is on file for you"})))
                    return

                ret = {
                    "success": True,
                    "cardNumber": credit[1][1],
                    "credit": credit[1][2],
                    "street": addr[1][1],
                    "city": addr[1][2],
                    "state": addr[1][3],
                    "zipcode": addr[1][4]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/payOrderNoAccount":
            # (InvID, CID, Card Number, Street, City, State, Zipcode, PID[] quantity[])
            if "invID" in params.keys() and "CID" in params.keys() and "cardNumber" in params.keys() and "PID" in params.keys() and "quantity" in params.keys():
                from ServerFilesCustomer.PaymentPage.placeOrder import placeOrder
                info = placeOrder(CONNECTION, int(params["CID"]), params['invID'], params["PID"], params["quantity"], cardNo=params["cardNumber"])
                print(info)
                ret = {
                    "success": info[0],
                    "trackingNumber": info[1],
                    "shipCompany": info[2],
                    "message": info[3]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/payOrderAccount":
            # (InvID, CID, Card Number, Street, City, State, Zipcode, PID[] quantity[])
            if "invID" in params.keys() and "CID" in params.keys() and "PID" in params.keys() and "quantity" in params.keys():
                from ServerFilesCustomer.PaymentPage.placeOrder import placeOrder
                info = placeOrder(CONNECTION, int(params["CID"]), params['invID'], params["PID"], params["quantity"])
                print(info)
                ret = {
                    "success": info[0],
                    "trackingNumber": info[1],
                    "shipCompany": info[2],
                    "message": info[3]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/accountModifyPR":
            # Get Credit card info
            # (Card Number, credit)
            # Get the email
            if "CID" in params.keys():
                from ServerFilesCustomer.ViewModifyAcc.requestAccInfo import requestAccInfo
                accInfo = requestAccInfo(CONNECTION, params["CID"]) # name, credit, address, orders, email

                from ServerFilesCustomer.PaymentPage.requestCredit import requestCredit
                credit = requestCredit(CONNECTION, params["CID"])

                ret = {
                    "success": True,
                    "message": "Gathered all items",
                    "cardNumber": credit[1][1],
                    "credit": credit[1][2],
                    "CID": params["CID"],
                    "name": accInfo[0][1],
                    "email": accInfo[4]
                }
                
                from ServerFilesCustomer.ViewModifyAcc.requestOrders import requestOrders
                orderHist = requestOrders(CONNECTION, accInfo[4]) # returned OrderID, Odate, total, status

                # Need to return (PID, ProductName, Quantity, Price)[]
                # (OrderID, day, month, year, total, tracking number, status)[]
                from ServerFilesCustomer.ViewModifyAcc.requestOrderDetails import requestOrderDetails
                hist = []
                for i in orderHist:
                    deets = requestOrderDetails(CONNECTION, accInfo[4], i[0]) # PID, ProductName, Quantity, price
                    t = {
                        "orderID": i[0],
                        "total": i[2],
                        "day": i[1].day,
                        "month": i[1].month,
                        "year": i[1].year,
                        "status": i[3],
                        "items": []
                    }
                    for j in deets:
                        t["items"].append({
                            "PID": j[0],
                            "pName": j[1],
                            "quantity": j[2],
                            "price": j[3]
                        })
                    hist.append(t)
                ret["orderHistory"] = hist
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))
        
        case "/customer/changeCredit":
            if "CID" in params.keys() and "cardNumber" in params.keys():
                from ServerFilesCustomer.ViewModifyAcc.changeCard import changeCard
                res = changeCard(CONNECTION, params["CID"], params["cardNumber"])
                if res[0]:
                    outStream.write(str.encode(json.dumps({"success": True, "cardNumber": res[1]})))
                else:
                    outStream.write(str.encode(json.dumps({"success": False,"message": res[1]})))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/changeAddress":
            if "CID" in params.keys() and "street" in params.keys() and "city" in params.keys() and "state" in params.keys() and "zipcode" in params.keys():
                from ServerFilesCustomer.ViewModifyAcc.changeAddress import changeAddress
                res = changeAddress(CONNECTION, params["CID"], params["street"], params["city"], params["state"], params["zipcode"])
                if res[0]:
                     outStream.write(str.encode(json.dumps({"success": True})))
                else:
                    outStream.write(str.encode(json.dumps({"success": False,"message": res[1]})))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/changePassword":
            if "CID" in params.keys() and "newPassword" in params.keys() and "oldPassword" in params.keys():
                from ServerFilesCustomer.ViewModifyAcc.changePassword import changePassword
                res = changePassword(CONNECTION, params["CID"], params["oldPassword"], params["newPassword"])
                outStream.write(str.encode(json.dumps({"success": res[0],"message": res[1]})))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/deleteAccount":
            if "CID" in params.keys():
                from ServerFilesCustomer.ViewModifyAcc.deleteAcc import deleteAcc
                res = deleteAcc(CONNECTION, params["CID"])
                outStream.write(str.encode(json.dumps({"success": res[0],"message": res[1]})))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        # Employees
        case "/employee/verifyLogin":
            if "EID" in params.keys() and "password" in params.keys():
                from ServerFilesEmployee.loginEmployee import loginVerificationEmployee
                res = loginVerificationEmployee(CONNECTION, params["EID"], params["password"])
                if res[0]:
                    outStream.write(str.encode(json.dumps({"success": True, "EID": res[1]})))
                else:
                    outStream.write(str.encode(json.dumps({"success": False, "message": res[1]})))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))
            
        case "/employee/storeStockPR":
            # Get inventories
            from ServerFilesEmployee.availableInv import availableInv
            invs = availableInv(CONNECTION)

            # Get product deets
            from ServerFilesEmployee.availableProd import availableProd
            prods = availableProd(CONNECTION)
            pro = []
            for i in prods:
                j = {
                    "PID": i[0],
                    "brandID": i[1],
                    "catID": i[2],
                    "name": i[3]
                }
                pro.append(j)

            # Get manufacturers
            from ServerFilesEmployee.manuInfo import manInfo
            mans = manInfo(CONNECTION)
            man = {}
            for i in mans:
                if i[0] in man.keys():
                    man[i[0]]["PID"].append(i[1])
                else:
                    man[i[0]] = { "manID": i[0], "PID": [i[1]], "capacity": i[3], "name": i[2] }


            # Take care of brands
            from ServerFilesCustomer.OnlineOrdering.BrandIDSearch import searchBrandID
            brands = searchBrandID(CONNECTION)

            # Take care of categories
            from ServerFilesCustomer.OnlineOrdering.CatIDSearch import searchCatID
            cats = searchCatID(CONNECTION)

            ret = {
                "success": True,
                "inv": invs,
                "products": pro,
                "mans": man,
                "brands": brands,
                "cats": cats
            }
            outStream.write(str.encode(json.dumps(ret)))

        case "/employee/viewInventory":
            if "invID" in params.keys():
                catID = params["catID"] if ("catID" in params.keys()) else False
                brandID = params["brandID"] if ("brandID" in params.keys()) else False
                from ServerFilesCustomer.OnlineOrdering.InvRequest import InvRequest
                search = InvRequest(CONNECTION, int(params["invID"]), brandID, catID)
                ret = []
                for i in search:
                    t = {
                        "PID": i[0],
                        "name": i[1],
                        "price": i[2],
                        "quant": i[3],
                        "brandName": i[4],
                        "catName": i[5]
                    }
                    ret.append(t)
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))
        
        case "/employee/manualRestock":
            if "invID" in params.keys() and "PID" in params.keys() and "quantity" in params.keys() and "manID" in params.keys() and "passkey" in params.keys():
                from ServerFilesEmployee.placeRestock import placeRestock
                res = placeRestock(CONNECTION, params["invID"], params["PID"], params["quantity"], params["manID"], params["passkey"]) # (True, RID, InvID, 'Restock Order placed.')
                ret = {
                    "success": res[0],
                    "restockID": res[1],
                    "invID": res[2],
                    "message": res[3]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "employee/inStoreOrderNoAccount":
            if "invID" in params.keys() and "PID" in params.keys() and "quantity" in params.keys():
                from ServerFilesEmployee.inStoreOrderNoAcc import inStoreOrderNoAcc
                res = inStoreOrderNoAcc(CONNECTION, params["invID"], params["PID"], params["quantity"])
                ret = {
                    "success": res[0],
                    "orderID": res[1],
                    "message": res[2]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "employee/inStoreOrderAccount":
            if "invID" in params.keys() and  "PID" in params.keys() and  "quantity" in params.keys() and  "email" in params.keys():
                from ServerFilesEmployee.inStoreOrderAcc import inStoreOrderAcc
                res = inStoreOrderAcc(CONNECTION, params["email"], params["invID"], params["PID"], params["quantity"])
                ret = {
                    "success": res[0],
                    "orderID": res[1],
                    "message": res[2]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))



class HANDLER(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        # get any paramaters out of the url

        pathStr = urlparse(self.path).path
        print("Pathing to", pathStr)

        params = parse_qs(urlparse(self.path).query)
        print("Paramaters are", params)


        # self.wfile.write(bytes("<html><body>Yoooo</body></html>", "utf-8"))
        try:
            with open("BrowserFiles" + pathStr, "rb") as f:
                if (pathStr[-3:] == "css"):
                    self.send_header("Content-type", "text/css")
                elif (pathStr[-4:] == "html"):
                    self.send_header("Content-type", "text/html")
                elif (pathStr[-2:] == "js"):
                    self.send_header("Content-type", "text/javascript")
                elif (pathStr[-3:] == "png"):
                    self.send_header("Content-type", "image/png")
                else:
                    print("ERROR: Mime type for " + pathStr + " is not defined")
                self.end_headers()
                self.wfile.write(bytearray(f.read()))
        except Exception as e:
            print("ERROR: Path " + pathStr + " failed")
            print(e)
            self.wfile.write(bytes("<html><body>The page you want either doesn't exist OR something went wrong</body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        pathStr = urlparse(self.path).path
        print("Pathing to", pathStr)

        datalen = int(self.headers['Content-Length'])
        data = self.rfile.read(datalen)
        a = json.loads(data)
        print("Paramaters are", a)


        handlePOST(pathStr, a, self.wfile)
        # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # self.wfile.write(bytes('{"time": "' + date + '"}', "utf-8"))

server = HTTPServer((HOST, PORT), HANDLER)
print("Server up and running captain")
server.serve_forever()
