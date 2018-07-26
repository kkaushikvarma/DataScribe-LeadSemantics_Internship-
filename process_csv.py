import datetime
import numpy as np
import numpy as np
from numpy import genfromtxt
import datetime
from math import *
import operator
import statistics
import random
import matplotlib
def sqr(x):
    return x*x
def distSquared(p1, p2):
    return sqr(p1[0] - p2[0]) + sqr(p1[1] - p2[1])

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.lengthSquared = distSquared(self.p1, self.p2)

    def getRatio(self, point):
        segmentLength = self.lengthSquared
        if segmentLength == 0:
            return distSquared(point, p1);
        return ((point[0] - self.p1[0]) * (self.p2[0] - self.p1[0]) + \
        (point[1] - self.p1[1]) * (self.p2[1] - self.p1[1])) / segmentLength

    def distanceToSquared(self, point):
        t = self.getRatio(point)
        if t < 0:
            return distSquared(point, self.p1)
        if t > 1:
            return distSquared(point, self.p2)

        return distSquared(point, [
            self.p1[0] + t * (self.p2[0] - self.p1[0]),
            self.p1[1] + t * (self.p2[1] - self.p1[1])
        ])

    def distanceTo(self, point):
        return math.sqrt(self.distanceToSquared(point))
    
    
class TrendObject:
    def __init__(self,nodes,tier,label,data = None):
        self.tier = tier
        self.raw = nodes
        self.x = (nodes[0][0],nodes[1][0])
        self.y = (nodes[0][1],nodes[1][1])
        self.parent = None
        self.children = []
        self.change = False
        self.data = data
        self.label = label

    def set_parent(self,parent):
        self.parent = parent
    def add_child(self,child):
        self.children.append(child)
    def merged_children(self):
        mn = 0
        for kid in self.children:
            if mn == 0:
                mn+=1
                p_slope = (kid.slope > 0)
            else:
                c_slope = (kid.slope > 0)
                if c_slope != p_slope:
                    mn+=1
        return(mn)
    def process(self,slope,period,length,local_max,local_min,x_range,y_range,gmin,gmax):
        self.slope = slope
        self.period = period
        self.length = length
        self.max = local_max
        self.min = local_min
        self.gmin = gmin
        self.gmax = gmax
        
        
        
class DataFrame_2D:
    def __init__ (self, label,data,recurs = None):
        self.label = label
        if recurs == None:
            self.data = data
            x, y = zip(*self.data)
            self.initial_date = x[0]
            self.int_data = list(zip(self.date_integers(x),y))
            self.x_range=(min(self.date_integers(x)),max(self.date_integers(x)))
            self.y_range=(min(y),max(y))
        else:
            self.x_range=(min([i[0] for i in data]),max([i[0] for i in data]))
            self.y_range=(min([i[1] for i in data]),max([i[1] for i in data]))
            self.initial_date = recurs
            self.int_data = data
            self.data = list(zip([self.initial_date+datetime.timedelta(days=i[0]) for i in self.int_data],[i[1] for i in self.int_data]))
        self.recurs = recurs
        self.weights = self.trend_data(self.int_data)
        if self.weights == None:
            self.trends = None
        else:
            self.remove_sterile_nodes()
            for tier in self.trends:
    #            print(self.trends.index(tier))
                self.populate_trend_nodes(tier)
        
    def date_integers(self,data):
        alk = data[0]
        return(list(map(lambda x: (x - alk).days,data)))
    def slope(self,x,y):
        slopes = []
        for i in range(len(x)-1):
            slopes.append((y[i+1]-y[i])/(x[i+1]-x[i]).days)
        return(slopes)
    def visualize(self, show = None):
        from matplotlib import pyplot as plt 
        f = plt.figure(figsize=(6,4))
        plt.title(self.label)
        if self.recurs != None:
            x = [self.initial_date+datetime.timedelta(days=i[0]) for i in self.int_data]
            y = [i[1] for i in self.int_data]
        else:
            x, y = zip(*self.data)
        dates = matplotlib.dates.date2num(x)
        plt.plot_date(dates, y, "b-")
        if show == None:
            plt.close()
        return(f)
    def trend_data(self,data):
        weights = self.simplifyDouglasPeucker(data)
        sorted_d = list(sorted(weights.items(), key=operator.itemgetter(1),reverse=True))
        tier_1 = sorted_d[:2]
        tier_2 = self.generate_tier_2(sorted_d,3)
        tier_3 = self.generate_tier(sorted_d[len(tier_2)+1:],1.0,7)
        if tier_3 == None:
            return(None)

        self.tiers = [list(sorted(([y[0] for y in tier_1]))),
                      list(sorted(list(set(([y[0] for y in tier_2]))))),
                      list(sorted(list(set(([y[0] for y in tier_1]+[y[0] for y in tier_2]+[y[0] for y in tier_3])))))]
        self.trends = [[TrendObject(self.tiers[0],0,self.label)]]
        def insert(a, tier):
            new_trends = []
            for x in self.trends[a]:
                sub_tier = tier[tier.index(x.raw[0]):tier.index(x.raw[1])+1]
                for i in range(len(sub_tier)-1):
                    node = (sub_tier[i],sub_tier[i+1])
                    obj = TrendObject(node,a+1,self.label,data[data.index(node[0]):data.index(node[1])+1])
                    obj.set_parent(x)
                    x.add_child(obj)
                    new_trends.append(obj)
            self.trends.append(new_trends)
                        
        insert(0,self.tiers[1])
        insert(1,self.tiers[2])
        self.store = []          
        def plot_tier(tier):
            data = [i[0] for i in tier]
            self.store += data
            data = list(sorted(self.store, key=lambda x: x[0]))
            
            x,y = zip(*data)
            plt.plot(x,y)
        return(weights)
    def generate_tier_2(self,data,max_nodes):
        def scale_x(node):
            return((node-self.x_range[0])/(self.x_range[1]-self.x_range[0]))
        def scale_y(node):
            return((node-self.y_range[0])/(self.y_range[1]-self.y_range[0]))
        points = []
        for point in data:
            no_way = False
            if len(points) < 2:
                points.append(point)
                continue
            else:
                for p2 in points:
                    if abs(scale_x(p2[0][0])-scale_x(point[0][0])) < 0.3:
                        no_way = True
                        break
                if no_way == True:
                    continue
                else:
                    points.append(point)
                    return(points)
    def generate_tier(self,data,threshold,max_nodes):
        def scale_x(node):
            return((node-self.x_range[0])/(self.x_range[1]-self.x_range[0]))
        def scale_y(node):
            return((node-self.y_range[0])/(self.y_range[1]-self.y_range[0]))
        points = []
        for point in data:
            no_way = False
            if len(points) < 2:
                points.append(point)
                continue
            else:
                for p2 in points:
                    if abs(scale_x(p2[0][0])-scale_x(point[0][0])) < 0.09:
                        no_way = True
                        break
            if no_way == True:
                continue
            else:
                n_points = points+[point]
                n_weights = [i[1] for i in n_points]
                coefvar = statistics.stdev(n_weights)/statistics.mean(n_weights)
                if coefvar < threshold and (len(points) < max_nodes):
                    points = n_points
                else:
                    return(points)
            
            
    def simplifyDouglasPeucker(self,points):
        weights = []
        length = len(points)

        def douglasPeucker(start, end):
            if (end > start + 1):
                line = Line(points[start], points[end])
                maxDist = -1
                maxDistIndex = 0

                for i in range(start + 1, end):
                    dist = line.distanceToSquared(points[i])
                    if dist > maxDist:
                        maxDist = dist
                        maxDistIndex = i

                weights.insert(maxDistIndex, maxDist)

                douglasPeucker(start, maxDistIndex)
                douglasPeucker(maxDistIndex, end)

        douglasPeucker(0, length - 1)
        weights.insert(0, float("inf"))
        weights.append(float("inf"))

        weightsDescending = weights
        weightsDescending = sorted(weightsDescending, reverse=True)
        
        return (dict(zip(points,weights)))
    def remove_sterile_nodes(self):
        for i, node in enumerate(self.trends[1]):
            if len(node.children) == 1:
                node.change = True
                try:
                    self.trends[1][i+1].add_child(node.children[0])
                    points = (node.raw[0],self.trends[1][i+1].raw[1])
                    self.trends[1][i+1].raw = points
                    self.trends[1][i+1].x = (points[0][0],points[1][0])
                    self.trends[1][i+1].y = (points[0][1],points[1][1])
                except:
                    self.trends[1][i-1].add_child(node.children[0])
                    try:
                        points = (self.trends[0][i-1].raw[1],node.raw[1])
                        self.trends[1][i-1].raw = points
                        self.trends[1][i-1].x = (points[0][0],points[1][0])
                        self.trends[1][i-1].y = (points[0][1],points[1][1])
                    except:
                        return
                self.trends[1][i] = node
    def populate_trend_nodes(self,tier_data):
        def scale_x(node):
            return((node-self.x_range[0])/(self.x_range[1]-self.x_range[0]))
        def scale_y(node):
            return((node-self.y_range[0])/(self.y_range[1]-self.y_range[0]))
        def get_unique_mm(m_list,tier):
            try:
                for point in m_list:
                    next_p = tier[tier.index(point)+1][1]-point[1]
                    prev_p = point[1]-tier[tier.index(point)-1][1]
                    if (next_p > 0 and prev_p > 0) or (next_p < 0 and prev_p < 0):
                        continue
                    else:
                        return(point)
            except:
                return(m_list[0])
                
                
        for node in tier_data:
#            node = tier_data[0]
            raw_tier = (self.int_data[self.int_data.index(node.raw[0]):self.int_data.index(node.raw[1])])
            
            local_max = max(raw_tier, key=operator.itemgetter(1))
            local_min = min(raw_tier, key=operator.itemgetter(1))
            gmax = get_unique_mm(sorted(raw_tier, key=operator.itemgetter(1),reverse = True),raw_tier)
            gmin = get_unique_mm(sorted(raw_tier, key=operator.itemgetter(1)),raw_tier)
            gmin = min(raw_tier, key=operator.itemgetter(1))
            gmax = max(raw_tier, key=operator.itemgetter(1))
            scaled_min = scale_x(local_min[0]),scale_y(local_min[1])
            scaled_max = scale_x(local_max[0]),scale_y(local_max[1])
            slope = (scale_y(node.y[1])-scale_y(node.y[0]))/(scale_x(node.x[1])-scale_x(node.x[0]))
            period = scale_x(node.x[1])-scale_x(node.x[0])
            max_dev = -(((slope*(scaled_max[0]-scale_x(node.x[0])))+scale_y(node.y[0]))-scaled_max[1])
            min_dev = ((slope*(scaled_min[0]-scale_x(node.x[0])))+scale_y(node.y[0]))-scaled_min[1]
            if abs(max_dev) < 0.15:
                local_max = None
            if abs(min_dev) < 0.15:
                local_min = None
            length = sqrt(pow(scale_y(node.y[1])-scale_y(node.y[0]),2)+pow(scale_x(node.x[1])-scale_x(node.x[0]),2))

            node.process(slope,period,length,local_max,local_min,self.x_range,self.y_range,gmin,gmax)
    def get_frame(self):
        return(self.trends)
class Process_CSV:
    def __init__(self,filename):
        self.data = open(filename,'r').read()
        self.labels_row = True
        self.labels = None
        self.x_axis = None
        self.y_axis = None
        self.variable_col = None
    def set_axis(self,axis,ind,dta_type,param):
        if type(ind) != int:
            ind = self.labels.index(axis[0])
        if axis == "x":
            self.x_axis = (ind,dta_type,param)
        if axis == "y":
            self.y_axis = (ind,dta_type,param)
    def transform(self):
        data = list(map(lambda x: x.split(','),self.data.split("\n")))
        if self.labels_row == True:
            self.labels = data[0]
            data = data[1:]
        if self.x_axis == None or self.y_axis == None:
            return "NaN"
        def ref_axis(axis,data):
            ind = axis[0]
            dta_type = axis[1]
            param = axis[2]
            def refine(node):
                if dta_type == 'datetime':
                    node[ind] = datetime.datetime.strptime(node[ind],param)
                elif dta_type == 'float':
                    node[ind] = float(node[ind])
                elif dta_type == 'int':
                    node[ind] = int(node[ind])
                return node
            return list(map(refine,data))
        
        data = ref_axis(self.x_axis,data)
        data = ref_axis(self.y_axis,data)
        self.data = np.asarray(data)
        self.dates = np.unique(self.data[:,1])
        if self.variable_col != None:
            variable_names = np.unique(self.data[:,0])
            dframes = []
            for n in range(variable_names.size):
                y = self.data[self.data[:, 0] == variable_names[n], :]
                y = y[:,1:].tolist()
                dframes.append((variable_names[n],y))
        return(dframes)
