
from threading import Thread
import threading
import time
import os
import logging
import dijkstra as dj


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s', )


class router_thread(Thread):

    def __init__(self, router, lock):
        Thread.__init__(self)
        self.on = True
        self.router = router
        self.hello_interval = 2
        self.lock = lock

    def write(self, s):
        self.router.buffer.write(s)

    def run(self):
        logging.debug('Router Thread Started Started')

        while(self.on):
            for i in range(5):
                time.sleep(self.hello_interval)

                for N, c in self.router.physical_connections.items():

                    logging.debug('sending to : ' + c['r'].name)

                    local_config = self.router.NIC_config[N]
                    with self.lock:
                        c['r'].send_hello(

                            {
                                #'version':'',
                                #'type':'hello',
                                #'packet_lenght':'',

                                'router_id': local_config['ip'],
                                'area_id': local_config['area'],

                                'Au_type': '0',  # no auth
                                #'checksum':'',

                                'network_mask': local_config['sn_mask'],
                                'router_priority': self.router.priority,

                                'hello_interval': self.hello_interval,
                                'dead_interval': '30',

                                'DR': '',
                                'BDR': '',
                                'Neighbour': self.router.neigbours.values(),
                                'options': {}
                            },
                            self.router

                        )
            with self.lock:
                G = self.router.creat_graph()
                d, E = dj.dijkestra(G, self.name)
                T = self.router.generate_routing_table(d, E)

                self.router.buffer.write('\nGenerated Graph :\n'+(
                    '*'*20) + '\n\n' + str(G) + '\n')
                self.router.buffer.write('\n\n' + (
                    '*'*20) + '\n\n' + str(d) + '\n\n' + str(E)+'\n')

                self.router.buffer.write('\n\nRouting Table' + (
                    '-'*20) + '\n\n' + str(T) + (
                        '-'*20) + '\n\n')


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
        # with self.lock:
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
        self.known_neighbors = []
        self.network_table = {}
        self.DR = self

        # threads running.
        self.router_thread = router_thread(router=self, lock=lock)
        self.router_thread.name = self.name

        # buffer writer to dispaly router debuging output.
        file_name = 'routers/' + name + '.txt'
        self.buffer = buffer_writer_thread(file_name, lock)

    def connect_physical(self, r, cost, lni, rni, pair=True):
        # simulate physical connection.
        # connects a router to a phyiscal NIC.
        # lni : local NIC index
        # rni : remote NIC index
        self.physical_connections[self.NIC_config.keys()[
                                  lni]] = {'r': r, 'cost': cost}

        logging.debug('Physical Connection {0} == > {1}'.format(
            self.name, r.name))

        if pair:
            r.connect_physical(self, cost, rni, lni, False)

    def __repr__(self):
        return self.name

    def send_hello(self, packet, sender):
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
            'Hello Recived ' + time.strftime('{%H:%M:%S}') + str(packet) + '\n')

        # check if same subnet
        # there are more checks than this
        # like hello intevral and dead intveraval
        # that need to mach but im not doing them for now at least .

        for N, c in self.physical_connections.items():

            if c['r'] not in self.known_neighbors:
                if c['r'].name == sender.name:
                    if True:  # self.NIC_config[N]['sn_mask'] == packet['network_mask']:
                        self.neigbours[sender.name] = c

                        self.known_neighbors.append(c['r'])

                        self.router_thread.write(
                            'Neighbour Added' + time.strftime('{%H:%M:%S} ') + packet['router_id'] + ' ' + sender.name + '\n')

                    break
            else:
                self.network_table[packet[
                    'router_id']] = packet['Neighbour']

                # self.router_thread.write(
                #     '\n\n\nCurrent Network Table' + str(self.network_table))
                self.creat_graph()

    def creat_graph(self):
        lkn = [self]  # list of known nodes
        G = {}

        for n in self.neigbours.values():
            if n['r'] not in lkn:
                lkn.append(n['r'])
                for m in n['r'].neigbours.values():
                    if m['r'] not in lkn:
                        lkn.append(m['r'])

        for i in xrange(len(lkn)):
            G[lkn[i].name] = {}

            for j in xrange(len(lkn)):
                G[lkn[i].name][lkn[j].name] = float('inf')
                if i == j:
                    G[lkn[i].name][lkn[j].name] = 0

                for n in lkn[i].physical_connections.values():
                    G[lkn[i].name][n['r'].name] = n['cost']

        return G

    def generate_routing_table(self, D, E):

        routing_table = []

        for n in E.keys():
            d = {}
            d['destination'] = n
            d['cost'] = D[n]
            d['gateway'] = E[n][1]

            routing_table.append(d)

        return routing_table


        # {'r4': 110, 'r5': 110,  'r2': 100, 'r3': 100}

        # {'r4': ('r4', 'r2'), 'r5': ('r5', 'r2'), 'r2': ('r2', 'r1'), 'r3': ('r3', 'r1')}


        # self.router_thread.write(
        #     '\nKnown Network Nodes' + str(G))

        # {'192.168.0.2': [{'r': r3, 'cost': 50}, {'r': r1, 'cost': 100}, {'r': r5, 'cost': 10}, {'r': r4, 'cost': 10}],

        #  '192.168.0.3': [{'r': r2, 'cost': 50}, {'r': r1, 'cost': 100}, {'r': r4, 'cost': 25}]}


def main():
    print 'PID ', os.getpid()

    lock = threading.RLock()

    r1 = router(name='r1', lock=lock)
    r1.NIC_config = {
        '00:00:00:00:01:01': {'ip': '192.168.0.1', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:01:02': {'ip': '192.168.0.1', 'sn_mask': '/24', 'area': '0'},
    }

    r2 = router(name='r2', lock=lock)
    r2.NIC_config = {
        '00:00:00:00:02:01': {'ip': '192.168.0.2', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:02': {'ip': '192.168.0.2', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:03': {'ip': '192.168.0.2', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:02:04': {'ip': '192.168.0.2', 'sn_mask': '/25', 'area': '0'},

    }

    r3 = router(name='r3', lock=lock)
    r3.NIC_config = {
        '00:00:00:00:03:01': {'ip': '192.168.0.3', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:03:02': {'ip': '192.168.0.3', 'sn_mask': '/24', 'area': '0'},
        '00:00:00:00:03:03': {'ip': '192.168.0.3', 'sn_mask': '/25', 'area': '0'},
    }

    r4 = router(name='r4', lock=lock)
    r4.NIC_config = {
        '00:00:00:00:04:01': {'ip': '192.178.1.5', 'sn_mask': '/25', 'area': '0'},
        '00:00:00:00:04:02': {'ip': '192.178.1.5', 'sn_mask': '/25', 'area': '0'},
    }

    r5 = router(name='r5', lock=lock)
    r5.NIC_config = {
        '00:00:00:00:04:01': {'ip': '192.122.1.4', 'sn_mask': '/25', 'area': '0'},
    }

    logging.debug("Created Routers")
    # link cost = 100 000 000 / 1 000 000
              #  100M / 1 MB = 100
    r1.connect_physical(r2, 100, 0, 0)
    r1.connect_physical(r3, 100, 1, 0)

    r2.connect_physical(r3, 50, 1, 1)
    r2.connect_physical(r4, 10, 3, 1)
    r2.connect_physical(r5, 10, 2, 0)

    r3.connect_physical(r4, 25, 2, 0)

    logging.debug("Coneected Routers")

    r1.buffer.start()
    r2.buffer.start()
    r3.buffer.start()
    r4.buffer.start()
    r5.buffer.start()

    r1.router_thread.start()
    r2.router_thread.start()
    r3.router_thread.start()
    r4.router_thread.start()
    r5.router_thread.start()


if __name__ == '__main__':
    main()
    raw_input()
    raw_input()
    os._exit(1)



    # r1 = router(name='r1', lock=lock)
    # r1.NIC_config = {
    #     '00:00:00:00:01:01': {'ip': '192.168.0.1', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:01:02': {'ip': '192.168.0.1', 'sn_mask': '/24', 'area': '0'},
    # }

    # r2 = router(name='r2', lock=lock)
    # r2.NIC_config = {
    #     '00:00:00:00:02:01': {'ip': '192.168.0.2', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:02:02': {'ip': '192.168.0.2', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:02:03': {'ip': '192.122.1.5', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:02:04': {'ip': '192.178.1.3', 'sn_mask': '/25', 'area': '0'},

    # }

    # r3 = router(name='r3', lock=lock)
    # r3.NIC_config = {
    #     '00:00:00:00:03:01': {'ip': '192.168.0.3', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:03:02': {'ip': '192.168.0.3', 'sn_mask': '/24', 'area': '0'},
    #     '00:00:00:00:03:03': {'ip': '192.178.1.4', 'sn_mask': '/25', 'area': '0'},
    # }

    # r4 = router(name='r4', lock=lock)
    # r4.NIC_config = {
    #     '00:00:00:00:04:01': {'ip': '192.178.1.5', 'sn_mask': '/25', 'area': '0'},
    #     '00:00:00:00:04:02': {'ip': '192.178.1.5', 'sn_mask': '/25', 'area': '0'},
    # }

    # r5 = router(name='r5', lock=lock)
    # r5.NIC_config = {
    #     '00:00:00:00:04:01': {'ip': '192.122.1.4', 'sn_mask': '/25', 'area': '0'},
    # }
