

class router(object):

    def __init__(self, area, ip, priority=1, connections=[], ):
        self.priority = priority
        self.ip = ip
        self.connections = connections
        self.area = area
        self.DR = self

        def network_connect(self, router):
            self.connections.append(router)
            router.connections.append(self)


def main():
    r1 = router(0, '192.168.0.1')
    r2 = router(0, '192.168.0.1')
    r3 = router(0, '192.168.0.1')
    r1.network_connect(r2)
    r1.network_connect(r3)


if __name__ == '__main__':
    main()
