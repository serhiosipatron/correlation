from django.http import HttpResponse
from django.template import RequestContext, loader
import math

class quantile :
    def t(p,v):
        u = quantile.U(p)
        g1 = 0.25 * (math.pow(u, 3) + u)
        g2 = 1.0 / 96 * (5 * math.pow(u, 5) + 16 * math.pow(u, 3) + 3 * u)
        g3 = 1.0 / 384 * (3 * math.pow(u, 7) + 19 * math.pow(u, 5) + 17 * math.pow(u, 3) - 15 * u)
        g4 = 1.0 / 92160 * (79 * math.pow(u, 9) + 779 * math.pow(u, 7) + 1428 * math.pow(u, 5) - 1920 * math.pow(u, 3) - 945 * u)
        return u + 1.0 / v * g1 + 1.0 / (v * v) * g2 + 1.0 / (v * v * v) * g3 + 1.0 / (v * v * v * v) * g4
    def U(p):
        return quantile.fi(p) if (p<= 0.5) else quantile.fi(1-p)
    def fi(a):
        t = math.sqrt(-2*math.log(a))
        c0 = 2.515517
        c1 = 0.802853
        c2 = 0.010328
        d1 = 1.432788
        d2 = 0.1892659
        d3 = 0.001308
        return t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)
    def F(alpha,v1,v2):
        pass


def index(request):

    Matrix = [[]]
    x = []
    y = []
    alpha = 0.05

    f = open('import.txt', 'r')
    for line in f:
        tmp = line.split(',')
        x.append(  float(tmp[0]))
        y.append(float(tmp[1]))
        Matrix.append([float(tmp[0]), float(tmp[1])])

    t = quantile.t(alpha*0.5,len(x)-1)

    sum = 0
    for xcount in x:
        sum += xcount
    xaverage = sum/len(x)
    sum = 0
    for ycount in y:
        sum += ycount
    yaverage = sum/len(x)

    avarageintervalX = [] # [averX-??, averX+??]
    avarageintervalY = []
    avarageintervalX.append(xaverage-t*xaverage/math.sqrt(len(x)))
    avarageintervalX.append(xaverage+t*xaverage/math.sqrt(len(x)))
    avarageintervalY.append(yaverage-t*yaverage/math.sqrt(len(y)))
    avarageintervalY.append(yaverage+t*yaverage/math.sqrt(len(y)))


    qwerty = 0
    for xcount in x :
        qwerty += math.pow(xcount - xaverage,2)
    stdx = math.sqrt(qwerty/(len(x)-1))
    qwer1 = 0
    for ycount in y :
        qwer1 += math.pow(ycount - yaverage, 2)
    stdy = math.sqrt( qwer1 / (len(y)-1))

    stdintervalX =[]
    stdintervalY =[]
    stdintervalX.append(stdx-t*xaverage/math.sqrt(len(x)*2))
    stdintervalX.append(stdx + t * xaverage / math.sqrt(len(x) * 2))
    stdintervalY.append(stdy - t * yaverage / math.sqrt(len(x) * 2))
    stdintervalY.append(stdy + t * yaverage / math.sqrt(len(x) * 2))

    ass = 0
    for xval in x :
        ass += math.pow((xval-xaverage),3)
    assimetr = ass/len(x) / math.pow(stdx,3)

    assimetry = 0
    for yval in y :
        assimetry += math.pow((yval-yaverage),3)
    assimetry = assimetry / (len(x) * math.pow(stdy,3))

    assimetrintervalX = []
    assimetrintervalY = []

    assimetrintervalX.append(assimetr-t*math.sqrt(6 * (1 - 12 / (2 * len(x) + 7)) / (len(x))))
    assimetrintervalX.append(assimetr + t*math.sqrt(6 * (1 - 12 / (2 * len(x) + 7)) / (len(x))))
    assimetrintervalY.append(assimetry - t*math.sqrt(6 * (1 - 12 / (2 * len(x) + 7)) / (len(x))))
    assimetrintervalY.append(assimetry + t*math.sqrt(6 * (1 - 12 / (2 * len(x) + 7)) / (len(x))))

    ex = 0
    for xval in x:
        ex += math.pow(xval-xaverage,4)
    excess = ex / len(x)  / math.pow(stdx,4)-3

    ex = 0
    for yval in y:
        ex += math.pow(yval - yaverage, 4)
    excessy = ex / len(y) / math.pow(stdy, 4)-3

    excessintervalX  =[]
    excessintervalY  =[]

    excessintervalX.append(excess-t*math.sqrt(24 * (1- 225 / (15* len(x))+124)) / len(x))
    excessintervalX.append(excess+t*math.sqrt(24 * (1 -225 / (15 * len(x)) + 124)) / len(x))
    excessintervalY.append(excessy-t*math.sqrt(24 * (1- 225 / (15* len(y))+124)) / len(y))
    excessintervalY.append(excessy+t*math.sqrt(24 * (1- 225 / (15* len(y))+124)) / len(y))
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'x': x,
        'y': y ,
        'n': len(x),
        'matrix': Matrix,
        'xaverage': xaverage,
        'yaverage': yaverage,
        'stdx': stdx,
        'stdy': stdy,
        'assimetr': assimetr,
        'assimetry': assimetry,
        'excess' : excess,
        'excy': excessy,
        'avarageintervalX':avarageintervalX,
        'avarageintervalY': avarageintervalY,
        'stdintervalX':stdintervalX,
        'stdintervalY':stdintervalY,
        'ass1': assimetrintervalX,
        'ass2': assimetrintervalY,
        'exsex1': excessintervalX,
        'exsex2': excessintervalY,
    })

    return HttpResponse(template.render(context))
