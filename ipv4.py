import socket
import concurrent.futures

class Ipv4Adress:
    def __new__(cls, __ip: str):
        if len(str(__ip).split(".")) == 4:
            for i in str(__ip).split("."):
                try:
                    if 0 <= int(i) <= 255:
                        return super().__new__(cls)
                except:
                    raise ValueError(f"The IPv4 address must follow the following format: 255.255.255.255\nAll bytes must be a number between 0 and 255.")
        else:
            raise ValueError(f"The IPv4 address must follow the following format: 255.255.255.255\nAll bytes must be a number between 0 and 255.")


    def __init__(self, __ip: str) -> None:
        self.__ip = __ip


    def __repr__(self) -> str:
        return f"Ipv4Adress('{self.__ip}')"
    

    def __str__(self) -> str:
        return str(self.__ip)
    
    
    def split(self, __arg = None) -> list:
        if __arg == None or __arg == "":
            return str(self.__ip).split(".")
        else:
            return str(self.__ip.split(__arg))


    def exist(self) -> bool:
        try:
            socket.gethostbyname(str(self.__ip))
            return True
        except socket.gaierror:
            return False


    def scan(self, max_scanning: int = 500, time_skip: int = 2) -> list:
        opened_port = []
        socket.setdefaulttimeout(time_skip)
        def run(port) -> None:
            scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if scanner.connect_ex((self.__ip, port)) == 0:
                opened_port.append(port)
            scanner.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_scanning) as executor:
            for port in range(65535):
                executor.submit(run, port + 1)

        return opened_port

def exist(ip: str or Ipv4Adress) -> bool:
    if str(type(ip)) == "<class 'str'>":
        Ipv4Adress(ip)
    try:
        socket.gethostbyname(ip)
        return True
    except socket.gaierror:
        return False

def get_ip(domaine) -> str:
    domaine: str
    try:
        return socket.gethostbyname(domaine)
    except:
        raise ValueError("This url doesn't exist")

def scan(ip: str or Ipv4Adress, max_scanning: int = 500, time_skip: int = 2) -> list:
    if str(type(ip)) == "<class 'str'>":
        Ipv4Adress(ip)
    opened_port = []
    socket.setdefaulttimeout(time_skip)
    def run(ip, port) -> None:
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if scanner.connect_ex((ip, port)) == 0:
            opened_port.append(port)
        scanner.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_scanning) as executor:
        for port in range(65535):
            executor.submit(run, ip, port + 1)

    return opened_port


class connection:
    def __init__(self, ip: str or Ipv4Adress, port: int, socket: socket.socket) -> None:
        if str(type(ip)) == "<class 'ipv4.Ipv4Adress'>":
            ip = str(ip)
        self.socket = socket
        self.addr = (ip, port)
        self.socket.connect(self.addr)
    

    def send(self, data: bytes or str) -> None:
        if str(type(data)) == "<class 'str'>":
            data = data.encode()
        self.socket.send(data)

    def finish(self) -> None:
        self.socket.close()


class TCPconnection(connection):
    def __init__(self, ip, port) -> None:
        super().__init__(ip=ip, port=port, socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM))


class UDPconnection(connection):
    def __init__(self, ip, port) -> None:
        super().__init__(ip=ip, port=port, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
