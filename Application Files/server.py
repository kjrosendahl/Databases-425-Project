from email.policy import default
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import io
import string
import time

HOST = "localhost"
PORT = 9999

def handlePOST(pathStr: str, params: dict, outStream: io.BufferedIOBase):
    match pathStr:
        case "customer/createAccount":
            from ServerFilesCustomer.customerCreateAcc import createAccount
            print("Creating a new account")
            result = createAccount(params.CID, params.email, params.password)
            # outStream.write()
    
def handleGET(pathStr: string, outStream: io.BufferedIOBase):
    match pathStr:
        case "/favicon.ico":
            print("Favicon requested")
            with open("BrowserFiles/favicon.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
                outStream.write(b)
        case "/customer/customerAccountCreation":
            print("Customer Account Creation Page")
            with open("BrowserFiles/Customers/customerAccountCreation.html", "rb") as f:
                outStream.write(bytearray(f.read()))
        case _: # Default case
            outStream.write(bytes("<html><body>The page you want doesn't exist</body></html>", "utf-8"))



class HANDLER(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # get any paramaters out of the url

        b = urlparse(self.path).path
        print("Pathing to", b)

        a = parse_qs(urlparse(self.path).query)
        print("Paramaters are", a)


        # self.wfile.write(bytes("<html><body>Yoooo</body></html>", "utf-8"))
        try:
            handleGET(b, self.wfile)
        except:
            print("beep")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        b = urlparse(self.path).path
        print("Pathing to", b)

        a = parse_qs(urlparse(self.path).query)
        print("Paramaters are", a)

        try:
            handlePOST(b, a, self.wfile)
        except:
            print("boop")
        # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # self.wfile.write(bytes('{"time": "' + date + '"}', "utf-8"))

server = HTTPServer((HOST, PORT), HANDLER)
print("Server up and running captain")
server.serve_forever()
