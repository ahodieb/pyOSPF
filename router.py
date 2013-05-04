
from threading import Thread
import time
import os


class router_thread(Thread):

    def __init__(self, buffer_writer):
        Thread.__init__(self)
        self.on = True
        self.buffer = buffer_writer.buffer

    def run(self):
        while(self.on):
            time.sleep(1)
            self.buffer.append(self.getName() + time.strftime('    {%H:%M:%S}'))


class buffer_writer_thread(Thread):

    def __init__(self, file_name):
        Thread.__init__(self)
        self.buffer = []
        self.buffer_write_interval = 5
        self.file_name = file_name
        self.on = True

    def run(self):
        while(self.on):
            time.sleep(self.buffer_write_interval)
            if self.buffer:  # to prevent opening the file if there is nothing to write.
                with open(self.file_name, 'a+b') as f:
                    while self.buffer:
                        f.write(self.buffer.pop(0) + '\n')


class router(object):

    def __init__(self, area, name, priority=1, connections=[], ):
        self.priority = priority
        self.connections = connections
        self.area = area
        self.DR = self
        self.name = name

        self.buffer_writer = buffer_writer_thread('routers/' + self.name + '.txt')
        self.router_thread = router_thread(self.buffer_writer)
        self.router_thread.name = self.name

    def network_connect(self, router):
        self.connections.append(router)
        router.connections.append(self)


def main():
    print 'PID ', os.getpid()

    r1 = router(0, 'r1')
    r2 = router(0, 'r2')
    r3 = router(0, 'r3')
    r1.network_connect(r2)
    r1.network_connect(r3)

    r1.buffer_writer.start()
    r1.router_thread.start()

    r2.buffer_writer.start()
    r2.router_thread.start()

    r3.buffer_writer.start()
    r3.router_thread.start()

if __name__ == '__main__':
    main()
    raw_input()
