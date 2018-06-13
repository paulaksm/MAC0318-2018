import numpy as np

class Robot():
    #        frente
    #       ---------
    #       |       |
    #       |       |
    #       |  LLL  |
    #       |  LLL  |
    #       ---------

    # idd, id do robo
    # xsize, largura do robo
    # xsize, comprimento do robo
    # xtag, distancia horizontal do lado esquerdo ao cento do tag
    # ytag, distancia vertical do topo ao cento do tag
    # posx, posy, course, posicao do robo
    def __init__(self, idd, xsize, ysize, xtag, ytag, posx = 0, posy = 0, course = 0):
        self.idd = idd
        self.xsize = xsize
        self.ysize = ysize
        self.xtag = xtag
        self.ytag = ytag

        self.posx = posx
        self.posy = posy
        self.course = course

    def lines(self):
        p1 = np.array([-self.xtag, self.ytag])
        p2 = np.array([-self.xtag, -self.ysize+self.ytag])
        p3 = np.array([self.xsize-self.xtag, self.ytag])
        p4 = np.array([self.xsize-self.xtag, -self.ysize+self.ytag])

        pos = np.array([self.posx, self.posy])

        c, s = np.cos(self.course), np.sin(self.course)
        R = np.array(((c,-s), (s, c)))

        p1 = p1.dot(R)+pos
        p2 = p2.dot(R)+pos
        p3 = p3.dot(R)+pos
        p4 = p4.dot(R)+pos
        return np.array([[p1, p2], [p2, p4], [p4, p3], [p1, p3]])

    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def line_intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    # get robot and see if this intersect te other
    def intersectRobot(self, robot):
        thislines = self.lines()
        other = robot.lines()
        for i in thislines:
            for j in other:
                if self.line_intersect(i[0], i[1], j[0], j[1]):
                    return True
        return False

        # get robot and see if this intersect te other
    def intersectLine(self, line):
        thislines = self.lines()
        for i in thislines:
            if self.line_intersect(i[0], i[1], (line[0], line[1]), (line[2], line[3])):
                    return True
        return False
