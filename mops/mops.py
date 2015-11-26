
class Mops:
    def __init__(self):
        pass

    def get_rdp_systems(self):
        rdp_port = 3389
        local_ip = socket.gethostbyname(socket.gethostname())
        local_ip = "10.0.0.232"
        ip_split = local_ip.split('.')
        base_ip = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2]
        for i in range(0, 256):
            url = "http://" + base_ip + '.' + str(i) + ":" + str(rdp_port)
            print(url)
            try:
                r = requests.get(url, timeout=3)
            except requests.exceptions.ConnectionError:
                print('ConnectionRefusedError')
                r = None
            if r:
                print(r)
                print(r.text())