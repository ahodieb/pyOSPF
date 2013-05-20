
from threading import Thread
import threading
import time
import os
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s', )


class router_thread(Thread):

    def __init__(self, router, lock):
        Thread.__init__(self)
        self.on = True
        self.router = router

    def write(self, s):
        self.router.buffer.write(s)

    def run(self):
        logging.debug('Router Started')
        while(self.on):
            time.sleep(2)

            for c in self.router.connections.values():
                logging.debug('sending to : ' + c['router'].name)
                c['router'].send_hello(

                    {
                        #'version':'',
                        #'type':'hello',
                        #'packet_lenght':'',

                        'router_id': '',
                        'area_id': '',

                        'Au_type': '0',  # no auth
                        #'checksum':'',

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

    def __init__(self, name, lock, priority=1):

        # configrations
        self.name = name
        self.priority = priority
        self.NIC_config = {}
        # ip assigned to each NIC ,
        # subnet mask.
        # area

        # connections
        self.physical_connections = {}

        # discoverd data.
        self.neigbours = {}
        self.DR = self

        # threads running.
        self.router_thread = router_thread(router=self, lock=lock)
        self.router_thread.name = self.name

        # buffer writer to dispaly router debuging output.
        file_name = 'routers/' + name + '.txt'
        self.buffer = buffer_writer_thread(file_name, lock)

    def connect_physical(self, r, lni, rni, pair=True):
        # simulate physical connection.
        # connects a router to a phyiscal NIC.
        # lni : local NIC index
        # rni : remote NIC index
        self.physical_connections[self.NIC_config.keys()[lni]] = r
        logging.debug('Physical Connection {0} == > {1}'.format(
            self.name, r.name))

        if pair:
            r.connect_physical(self, rni, lni, False)

    def send_hello(self, p):
        """
        {
        ##header##
        'version':'',
        'type':'hello',
        'packet_lenght':'',
        'router_id':'',
        'area_id':'',
        'Au_type':'',
        'checksum':'',

        ##Hello Packet
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


def main():
    print 'PID ', os.getpid()

    lock = threading.RLock()

    r1 = router(name='r1', lock=lock)
    r1.NIC_config = {
        '00:00:00:00:01:01': {'ip': '192.168.0.4', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:01:02': {'ip': '192.168.0.5', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:01:03': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:01:04': {'ip': '192.168.0.7', 'sn_mask': '/24', 'area': '0'},
    }

    r2 = router(name='r2', lock=lock)
    r2.NIC_config = {
        '00:00:00:00:02:01': {'ip': '192.168.0.4', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:02': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:03': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:04': {'ip': '192.168.0.7', 'sn_mask': '/24', 'area': '0'},
    }

    r3 = router(name='r3', lock=lock)
    r3.NIC_config = {
        '00:00:00:00:03:01': {'ip': '192.168.0.4', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:03:02': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:03:03': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:03:04': {'ip': '192.168.0.7', 'sn_mask': '/24', 'area': '0'},
    }

    r4 = router(name='r4', lock=lock)
    r4.NIC_config = {
        '00:00:00:00:04:01': {'ip': '192.168.0.4', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:04:02': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:04:03': {'ip': '192.168.0.6', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:04:04': {'ip': '192.168.0.7', 'sn_mask': '/24', 'area': '0'},
    }

    logging.debug("Created Routers")

    r1.connect_physical(r2, 0, 0)
    r1.connect_physical(r3, 1, 0)
    r1.connect_physical(r4, 2, 0)

    logging.debug("Coneected Routers")

    # r1.router_thread.start()
    # r2.router_thread.start()
    # r3.router_thread.start()


if __name__ == '__main__':
    main()
    raw_input()
