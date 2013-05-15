
from threading import Thread
import threading
import time
import os
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s', )


class router_thread(Thread):

    def __init__(self, router, name, lock):
        Thread.__init__(self)
        self.on = True
        file_name = 'routers/' + name + '.txt'
        self.buffer = buffer_writer_thread(file_name, lock)
        self.buffer.start()
        self.router = router

    def write(self, s):
        self.buffer.write(s)

    def run(self):
        logging.debug('Router Started')
        while(self.on):
            time.sleep(2)

            for c in self.router.connections.values():
                logging.debug('sending to : ' + c['router'].name)
                c['router'].send_hello(

                    {
                        'network_mask': '255.255.255.0',
                        'router_priority': '1',

                        'hello_interval': '10',
                        'dead_interval': '30',

                        'DR': '',
                        'BDR': '',
                        'Neighbour': self.router.connections.keys(),
                        'options': {}
                    }

                )

            # self.buffer.append(self.getName() + time.strftime('
            # {%H:%M:%S}'))


class buffer_writer_thread(Thread):

    def __init__(self, file_name, lock):
        Thread.__init__(self)
        self.buffer = []
        self.buffer_write_interval = 5
        self.file_name = file_name
        self.lock = lock
        self.on = True

    def write(self, s):
        # logging.debug('writing to output buffer.')
        with self.lock:
            self.buffer.append(s)
            # logging.debug(s)

    def dump(self):
        # locking the thread to write affects the performance !
        # logging.debug('Dumping buffer to files.')
        # logging.debug(self.buffer)

        with self.lock:
            if self.buffer:
                with open(self.file_name, 'a+b') as f:
                    while self.buffer:
                        f.write(self.buffer.pop(0) + '\n')

    def run(self):
        while(self.on):
            time.sleep(2)
            self.dump()


class router(object):

    def __init__(self, area, name, lock, priority=1, connections=[], ):
        self.priority = priority
        self.connections = connections
        self.area = area
        self.DR = self
        self.name = name
        self.connections = {}

        self.router_thread = router_thread(router=self, name=name, lock=lock)
        self.router_thread.name = self.name

    def connect(self, connection):
        self.connections[connection['ip']] = connection

    def send_hello(self, p):
        """
        {
        'network_mask':'',
        'router_priority':'',

        'hello_interval':'',
        'dead_interval':'',

        'DR':'',
        'BDR':'',
        'Neighbour':[]
        'options':{}
        }
        """
        self.router_thread.write(
            'Hello Recived ' + time.strftime('{%H:%M:%S}') + str(p) + '\n')

    def setup_connection(router, ip, subnet_mask, connection_type, NIC, note=''):
        """
        Parameters
        ----------
        router : router object
                 The router object to be connected.
        ip : str
             The ip of this router in this connection.
        subnet_mask : str
                      The ip of this router in this connection.
        connection_type : str
                          the type of connection ex: p2p ,switch, frame realy , other .
        NIC : str
              the NIC mac address of the connection.

        """

        return {'router': router, 'ip': ip, 'subnet_mask': subnet_mask, 'connection_type': connection_type, 'NIC': NIC, 'note': note}


def main():
    print 'PID ', os.getpid()

    lock = threading.RLock()

    r1 = router(area=0, name='r1', lock=lock)
    r2 = router(area=0, name='r2', lock=lock)
    r3 = router(area=0, name='r3', lock=lock)

    logging.debug("Created Routers")

    r1.connect(router.setup_connection(
        r2, '192.168.0.4', '255.255.255.0', 'p2p', '90:E6:BA:88:18:3A'))

    r1.connect(router.setup_connection(
        r3, '192.168.0.5', '255.255.255.0', 'p2p', '00:02:21:04:43:21'))

    logging.debug("Coneected Routers")

    r1.router_thread.start()
    r2.router_thread.start()
    r3.router_thread.start()

if __name__ == '__main__':
    main()
    raw_input()
