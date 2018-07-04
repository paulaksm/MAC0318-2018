import socket
import sys
import threading
import numpy as np
from socket import error as SocketError
from robot import Robot
import time

# intervalo do jogo
run_time = 5

class TagServer(threading.Thread):
    def __init__(self, port, board_size, maplines):
        threading.Thread.__init__(self)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('0.0.0.0', port)
        print ('Starting up on %s port %s' % server_address)
        sock.bind(server_address)
        sock.listen(1)

        sock.settimeout(1)
        self.sock = sock
        self.clients_threads = []

        self.tag = None
        self.board_size = board_size
        self.map = maplines

        self.paused = True
        self.runV = True

        self.last = 0
        self.mutex = threading.Lock()
        self.mutex2 = threading.Lock()
        self.start()

    def updatePosition (self, idd, posx, posy, course):
        self.mutex.acquire()
        clients_threads = self.clients_threads
        self.mutex.release()
        for thread in clients_threads:
            if thread.robot is not None and thread.robot.idd == idd:
                msg = "P "
                msg = msg + str(posx)+","
                msg = msg + str(posy)+","
                msg = msg + str(course)+","
                msg = msg + str(thread.robot.idd)+","
                msg = msg + str(thread.robot.xsize)+","
                msg = msg + str(thread.robot.ysize)+","
                msg = msg + str(thread.robot.xtag)+","
                msg = msg + str(thread.robot.ytag)
                thread.robot.posx = posx
                thread.robot.posy = posy
                thread.robot.course = course
                self.brodcast(msg)

        # check for collision
        self.mutex2.acquire()
        for i in self.robots():
            for line in self.map:
                if i.intersectLine(line):
                    print(i.idd, " PAUSE")
                    self.brodcast("PAUSE "+str(i.idd))
                    break

            # se nao eh o pegador continua
            if i == self.tag:
                continue
            # verifica se colidiu
            for j in self.robots():
                if i == j:
                    continue
                if i.intersectRobot(j):
                    if self.last + run_time <= time.time():
                        print(i.idd, " pegou ", j.idd)
                        self.tag = j
                        self.brodcast("RUN "+str(self.tag.idd)+","+str(run_time))
                        self.last = time.time()
                        break

        self.mutex2.release()

    def stopGame (self):
        self.paused = True
        self.brodcast("STOP")

    def startGame (self):
        self.brodcast("START")
        r = self.robots()
        if len(r) >= 1:
            tag = np.random.choice(r, 1)
            self.tag = tag[0]
            self.paused = False
            self.brodcast("RUN "+str(self.tag.idd)+","+str(run_time))

    def brodcast(self, msg):
        self.mutex.acquire()
        clients_threads = self.clients_threads
        self.mutex.release()
        for thread in clients_threads:
            if thread.robot is not None:
                thread.send(msg+"\n")

    def run(self):
        while self.runV:
            try:
                (clientsock, (ip, port)) = self.sock.accept()
                newthread = TagThread(ip, port, clientsock, self)
                self.mutex.acquire()
                self.clients_threads.append(newthread)
                self.mutex.release()
                self.stopGame()
            except socket.timeout as err:
                pass
        self.sock.close()

    def robots(self):
        r = []
        self.mutex.acquire()
        clients_threads = self.clients_threads
        self.mutex.release()
        for thread in clients_threads:
            if thread.robot is not None:
                r.append(thread.robot)
        return r

    def stop(self):
        self.brodcast("QUIT")
        self.mutex.acquire()
        clients_threads = self.clients_threads
        self.mutex.release()
        for thread in clients_threads:
            thread.stop()
        self.runV = False


class TagThread(threading.Thread):

    def __init__(self, ip, port, socket, server):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = socket

        self.points = 0

        self.robot = None
        self.bz = server.board_size
        self.map = server.map
        self.server = server

        socket.settimeout(1)
        self.runV = True
        self.mutex = threading.Lock()
        self.start()


    def run(self):
        while self.runV:
            try:
                data = self.sock.recv(128).decode('ascii')
            except socket.timeout as err:
                continue
            except SocketError as e:
                self.robot = None
                break
            data = data.split("\n")[0]
            data = data.split(" ")
            try:
                # print (data)
                if data[0] == "SUB":
                    idd, xsize, ysize, xtag, ytag = data[1].split(",")
                    self.robot = Robot(int(idd), float(xsize), float(ysize), float(xtag), float(ytag))
                    m = str(self.map).replace(", ", ":")
                    self.send("OK "+str(self.bz[0])+","+str(self.bz[1])+","+m+"\n")
                if data[0] == "P":
                    posx, posy, curse = data[1].split(",")
                    posx, posy, curse = float(posx), float(posy), float(curse)
                    self.server.updatePosition(self.robot.idd, posx, posy, curse)
            except Exception as e:
                raise
                self.send("ERR\n")
        self.sock.close()

    def send(self, msg):
        self.mutex.acquire()
        try:
            self.sock.sendall(msg.encode('ascii'))
        except SocketError as e:
            pass
        self.mutex.release()

    def stop(self):
        self.runV = False

class TagClient(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        sock.connect(server_address)
        sock.settimeout(1)
        self.sock = sock
        self.stopf = None
        self.startf = None
        self.runf = None
        self.position = None
        self.pause = False

        # info
        self.runing = False
        self.tag = None
        self.positions = []
        self.board = None

        self.maplines = None

        self.quit = False

        self.mutex = threading.Lock()

    def info (self, idd, xsize, ysize, xtag, ytag):
        idd, xsize, ysize, xtag, ytag = str(idd), str(xsize), str(ysize), str(xtag), str(ytag)
        message = "SUB "+idd+","+xsize+","+ysize+","+xtag+","+ytag+"\n"
        self.sock.sendall(message.encode('ascii'))
        self.runV = True
        self.start()

    def run(self):
        data = ""
        while self.runV:
            try:
                data += self.sock.recv(256).decode('ascii')
            except socket.timeout as err:
                continue
            except SocketError as e:
                self.robot = None
                break

            if "\n" not in data:
                continue

            splitdata = data.split("\n")
            if splitdata[-1] != '':
                data = splitdata[-1]
                splitdata = splitdata[0:-1]
            else:
                data = ""

            for d in splitdata:
                d = d.split(" ")
                if d[0] == "OK":
                    x, y, lines = d[1].split(",")
                    x, y = float(x), float(y)
                    self.maplines = []
                    lines = lines.replace("[[", "")
                    lines = lines.replace("]]", "")
                    lines = lines.split("]:[")
                    for line in lines:
                        if line == '[]':
                            continue
                        points = [float(p) for p in line.split(":")]
                        a, b, c, d = points
                        self.maplines.append([a, b, c, d])
                    x, y = y, x
                    self.maplines.append([0, 0, x, 0])
                    self.maplines.append([x, 0, x, y])
                    self.maplines.append([0, 0, 0, y])
                    self.maplines.append([0, y, x, y])
                    print(self.maplines)
                    self.board = (x, y)

                elif d[0] == "P":
                    posx, posy, course, idd, xsize, ysize, xtag, ytag = d[1].split(",")
                    posx = float(posx)
                    posy = float(posy)
                    course = float(course)
                    idd = int(idd)
                    xsize = float(xsize)
                    ysize = float(ysize)
                    xtag = float(xtag)
                    ytag = float(ytag)

                    self.mutex.acquire()
                    self.positions.append((posx, posy, course, idd, xsize, ysize, xtag, ytag))
                    self.mutex.release()

                elif d[0] == "START":
                    print(d)
                    self.runing = True

                elif d[0] == "STOP":
                    print(d)
                    self.runing = False

                elif d[0] == "RUN":
                    print(d)
                    idd, interval = d[1].split(",")
                    self.tag = (int(idd), float(interval)+time.time())
                elif d[0] == "QUIT":
                    print(d)
                    self.stop()
                elif d[0] == "PAUSE":
                    print(d)
                    self.pause = True
        self.sock.close()
        self.quit = True

    def getStatus(self):
        return self.runing

    def isPause(self):
        return self.pause

    def setPause(self):
        self.pause = False

    def getFieldInfo(self):
        return self.board;

    def getMapLines(self):
        return self.maplines;

    def getPosition(self):
        i = self.positions
        self.mutex.acquire()
        self.positions = []
        self.mutex.release()
        return i

    def getTagInfo(self):
        return self.tag

    # Somente na simulacao
    def setPosition(self, px, py, course):
        message = "P "+str(px)+","+str(py)+","+str(course)+"\n"
        self.sock.sendall(message.encode('ascii'))

    def stop(self):
        self.runV = False
