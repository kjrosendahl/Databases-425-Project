from http.server import HTTPServer, BaseHTTPRequestHandler
import imp
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
    print("posting")
    match pathStr:
        case "/customer/createCustomer":
            print("Creating Customer")
            from ServerFilesCustomer.customerCreateRecord import newCustomerRecord
            acc = newCustomerRecord(CONNECTION, params["name"])
            print(acc)
            ret = {
                "success": acc[0],
                "CID": acc[1]
            }
            outStream.write(str.encode(json.dumps(ret)))

        case "/customer/verifyLogin":
            print("Veriftying login information")
            if "email" in params.keys() and "password" in params.keys():
                from ServerFilesCustomer.customerLogin import loginVerification
                acc = loginVerification(CONNECTION, params["email"], params["password"])
                ret = {
                    "success": acc[0],
                    "CID": acc[1]
                }
                outStream.write(str.encode(json.dumps(ret)))
            else:
                print("Incorrect data")
                outStream.write(str.encode(json.dumps({"success": False,"message": "Incorrect number of arguments"})))

        case "/customer/createAccount":
            print("Creating Online Account")
            # First check if we have the correct data
            if "CID" in params.keys and "email" in params.keys and "password" in params.keys and "cardNumber" in params.keys and "CVV" in params.keys and "street" in params.keys and "city" in params.keys and "state" in params.keys and "zipcode" in params.keys:
                
                # First create the onlineAcc
                from ServerFilesCustomer.customerCreateAcc import createAccount
                acc = createAccount(CONNECTION, params["CID"], params["email"], params["password"])
                print(acc)

                # Add the credit card
                from ServerFilesCustomer.customerCreateCard import createCreditCard
                card = createCreditCard(CONNECTION, params["CID"], params["cardNumber"], params["CVV"])
                print(card)
                
                # Add the address
                from ServerFilesCustomer.customerCreateAddress import createAddress
                addr = createAddress(acc["CID"], params["street"], params["city"], params["state"], params["zipcode"])
                print(addr)
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
        
        case "/customer/addAddress":
            print("Adding Address")
            if "CID" in params.keys() and "street" in params.keys() and "city" in params.keys() and "state" in params.keys() and "zipcode" in params.keys():
                from ServerFilesCustomer.customerCreateAddress import createAddress
                addr = createAddress(CONNECTION, params["CID"], params["street"], params["city"], params["state"], params["zipcode"])
                print(addr)
                ret = {
                    "success": addr[0],
                    "CID": addr[1],
                    "message": addr
                }



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
