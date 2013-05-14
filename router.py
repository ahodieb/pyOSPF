
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
        self.buffer = []
        self.lock = lock
        self.file_name = 'routers/' + name + '.txt'
        self.router = router

    def dump(self):
        # locking the thread to write affects the performance !
        logging.debug('Dumping buffer to files.')
        logging.debug(self.buffer)

        with self.lock:
            if self.buffer:
                with open(self.file_name, 'a+b') as f:
                    while self.buffer:
                        f.write(self.buffer.pop(0) + '\n')

    def write(self, s):
        logging.debug('writing to output buffer.')
        with self.lock:
            self.buffer.append(s + '      ' + time.strftime('{%H:%M:%S}'))
            logging.debug(s)

    def run(self):
        while(self.on):
            time.sleep(1)
            logging.debug('Router Started')
            self.write('hi')
            time.sleep(1)
            self.write('hello')
            time.sleep(2)
            self.dump()
            # self.buffer.append(self.getName() + time.strftime('
            # {%H:%M:%S}'))


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

    def setup_connection(router, ip, connection_type, NIC, note=''):
        return {'router': router, 'ip': ip, 'connection_type': connection_type, 'NIC': NIC, 'note': note}


def main():
    print 'PID ', os.getpid()

    lock = threading.RLock()

    r1 = router(area=0, name='r1', lock=lock)
    r2 = router(area=0, name='r2', lock=lock)
    r3 = router(area=0, name='r3', lock=lock)

    logging.debug("Created Routers")

    logging.debug(router.setup_connection(
        r2, '192.168.0.4', 'eth', '90:E6:BA:88:18:3A'))

    r1.connect(router.setup_connection(
        r2, '192.168.0.4', 'eth', '90:E6:BA:88:18:3A'))

    r1.connect(router.setup_connection(
        r3, '192.168.0.4', 'eth', '00:02:21:04:43:21'))

    logging.debug("Coneected Routers")

    r1.router_thread.start()
    r2.router_thread.start()
    r3.router_thread.start()

if __name__ == '__main__':
    main()
    raw_input()
