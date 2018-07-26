import random
import datetime
import textwrap
class Constructor:
    def __init__(self,trends):
        self.label = trends.label
        self.initial_date = trends.initial_date
        self.trends = trends.get_frame()
        state_1 = random.randint(0, 1)
        if state_1 == 0:
            state_2 = 1
        else:
            state_2 = 0
        sentence = []
        for index,trend in enumerate([i for i in self.trends[1] if self.classify_type(i)!= None]):  
            if index == 0:
                if trend.slope > 0:
                    prev_node = 1
                else:
                    prev_node = 0
                if len(self.trends[1]) > 1:
                    sentence.append(self.process(trend,None,state_1))
                else:
                    sentence.append(self.process(trend,None,state_1))
            else:
                if trend.slope > 0:
                    c_node = 1
                else:
                    c_node = 0
                if c_node == prev_node:
                    sentence.append(self.process(trend,True,state_2))
                else:
                    sentence.append(self.process(trend,True,state_2,True))
                prev_node = c_node
        cr = None
        self.datex = (str(sentence[0].sdate)+" - "+str(sentence[-1].edate))
        sentence = [i.to_string() for i in sentence]
        for ind, i in enumerate(sentence):
            if self.label in i:
                if cr == None:
                    cr = True
                    continue
                else:
                    sentence[ind] = sentence[ind].replace(str(self.label),"it")
                    
        self.get_string = [textwrap.fill(i) for i in sentence]

        
                    
                
        
    def classify_type(self,node):
        children = [i for i in node.children if i.period >= 0.05]
        if node.change == True or node.period < 0.1:
            return(None)
        if (len(node.children)) < 3:
            return('constant')
        inc_children = [i for i in children if i.slope > 0.0]
        dec_children = [i for i in children if i.slope < 0.0]
        if len(inc_children) == 0 or len(dec_children) == 0:
            return('exaggerate')
        inc_val = (sum([i.length for i in inc_children]))/(sum([i.length for i in dec_children])+sum([i.length for i in inc_children]))
        if (inc_val < 0.35 or inc_val > 0.65):
            if inc_val < 0.10 or inc_val > 0.90:
                return('constant')
            return('exception')
        else:
            if node.merged_children() < 4:
                return('step')
            else:
                return('series')
            
    def get_mm(self,mm):
        add_node = []
        lmax = mm[0]
        lmin = mm[1]
        if lmax != None and lmin != None:
            if lmax[0] < lmin[0]:
                n1 = [0,lmax[1],self.date_trans(lmax[0],2)]
                n2 = [1,lmin[1],self.date_trans(lmin[0],2)]
            else:
                n1 = [1,lmin[1],self.date_trans(lmin[0],2)]
                n2 = [0,lmax[1],self.date_trans(lmax[0],2)]
            add_node=[n1,n2]
        else:
            if lmax != None:
                add_node.append([0,lmax[1],self.date_trans(lmax[0],2)])
            if lmin != None:
                add_node.append([1,lmin[1],self.date_trans(lmin[0],2)])
            else:
                add_node = None
        return(add_node)
            
    
    def date_trans(self,dt_numb,param):
        dt = self.initial_date+datetime.timedelta(days=dt_numb)
        
        if param == 2:
            return(dt.strftime('%b')+" "+str(dt.strftime('%Y')))
        else:
            return(str(dt.strftime('%Y')))
    
    def process(self,node,priority,state,mod = None):
        cat = self.classify_type(node)
        children = [i for i in node.children if i.period > 0.09]
        fix_state = None
        add_node = []
        if cat == None:
            return(None)
        if cat == "constant":
            add_node = self.get_mm((node.max,node.min))   
        if cat == "exaggerate":
            add_node = []
            for lnode in children:
                if node.slope > 0:
                    gg = lnode.gmax
                    try:
                        exception = [[1,lnode.min[1],self.date_trans(lnode.min[0],2)]]
                    except:
                        exception = None
                else:
                    gg = lnode.gmin
                    try:
                        exception = [[0,lnode.max[1],self.date_trans(lnode.max[0],2)]]
                    except:
                        exception = None
                an = [gg[1],self.date_trans(gg[0],2)]
#                exception = self.get_mm((lnode.max,lnode.min))
                add_node.append([an,exception])            
        if cat == "exception":
            mlen = 0
            for lnode in node.children:
                if lnode.slope < 0 and node.slope > 0 or (lnode.gmin[1] == 15.81):
                    if mlen < abs(lnode.length):
                        add_node = [1,lnode.gmin[1],self.date_trans(lnode.gmin[0],2)]
                        mlen = abs(lnode.length)
                if lnode.slope > node.slope < 0:
                    
                    if mlen < abs(lnode.length):
                        add_node = [0,lnode.gmax[1],self.date_trans(lnode.gmax[0],2)]
                        mlen = abs(lnode.length)               
#        if cat == "exception":
#            if node.slope > 0:
#                add_node = [1,node.gmin[1],self.date_trans(node.gmin[0],2)]
#            else:
#                add_node = [0,node.gmax[1],self.date_trans(node.gmax[0],2)]          
                        
        if cat == "step":
            add_node = []
            mx = node.gmax
            mn = node.gmin

            
            mx = None
            mn = None
            for lnode in [i for i in node.children if i.period > 0.05]:
                if lnode.slope > 0:
                    if mx == None or mx[1] < lnode.gmax[1]:
                        mx = lnode.gmax
                else:
                    if lnode.slope < 0:
                        if mn == None or mn[1] > lnode.gmin[1]:
                            mn = lnode.gmin
            if mx[0] < mn[0]:
                add_node.append([0,mx[1],self.date_trans(mx[0],2)])
                add_node.append([1,mn[1],self.date_trans(mn[0],2)])
            else:
                add_node.append([1,mn[1],self.date_trans(mn[0],2)])
                add_node.append([0,mx[1],self.date_trans(mx[0],2)])
        if cat == "series":
            add_node = self.get_mm((node.max,node.min))  
        
        if node.slope > 1.0:
            grate = 1 
        elif node.slope > 0.3:
            grate = 2
        else:
            grate = 3
        if node.slope > 0:
            change = 0
        else:
            change = 1
        if abs(node.x[0]-node.x[1]) < 1200:
            param = 2
        else:
            param = 0
        rangex = [node.y,[self.date_trans(node.x[0],param),self.date_trans(node.x[1],param)]]
        if cat == "exception":
            if change == 0:
                if int(add_node[1])>=rangex[0][1]:
                    cat = "constant"
                    add_node = None
            else:
                if int(add_node[1])<=rangex[0][0]:
                    cat = "constant"
                    add_node = None
                
        
        data = [cat,add_node,grate,change,rangex]
        
        sentence = parse(data,self.label,state,priority,mod)
        return(sentence)
    
    
    
    
    
    
            
class parse:
    def __init__(self,data,lb,state,priority,modifier = None):
        import random
        self.previous_change = None
        self.cat = data[0]
        self.additional = data[1]
        self.state = state
        self.grate = data[2]
        self.lb =    lb
        self.changex =data[3]
        rangex = data[4]
        self.iv = str(int(rangex[0][0]))
        self.fv = str(int(rangex[0][1]))
        if self.iv == self.fv:
            self.iv = str((rangex[0][0]))
            self.fv = str((rangex[0][1]))
        self.perc = str(abs(int((rangex[0][1]-rangex[0][0])/rangex[0][0]*100)))
        self.sdate = rangex[1][0]
        self.edate = rangex[1][1]
        self.priority = priority
        self.modifier = modifier
        self.sentence = self.prime()
        
        
    def to_string(self):
        return(self.string_filters(" ".join(self.sentence)))
    def string_filters(self,ns):
        ns=ns.replace("  ", " ")
        ns=ns.replace("$ ", "$")
        ns=ns.replace(" .", ".")
        ns=ns.replace(",,", ",")
        ns=ns.replace(" ,", ",")
        ns = ns[0].capitalize()+ns[1:]
        if ns[-1] != ".":
            ns = ns+"."
        return(ns)
    def transition(self):
        return(random.choice(["However,", "On the contrary,", "Nevertheless,"]))
    def prime(self):
        if self.additional == None:
            if self.modifier == True:
                return([self.transition()]+self.gen_sent())
            return(self.gen_sent())
        else:
            if self.modifier == True:
                return([self.transition()]+self.tot_sent())
            return(self.tot_sent())
    def tot_sent(self):
        if (self.cat == "constant" or self.cat == "exception" or self.cat == "series"):
            if self.priority == True:
                content = [self.gen_sent()+[","]+self.add_sent()]
            elif self.priority == False:
                content = [self.add_sent()+[","]+self.gen_sent()]
            else:
                content = [self.add_sent()+[","]+self.gen_sent(),self.gen_sent()+[","]+self.add_sent()]
        else:
            content = [self.gen_sent("nod")+["."]+self.add_sent()]
        return(random.choice(content))
    def add_sent(self):
        if self.cat == "constant" or self.cat == "series":
            return(self.constant())
        elif self.cat == "exception":
            return(self.exception())
        elif self.cat == "exaggerate":
            return(self.exaggeration())
        elif self.cat == "step":
            return(self.step())
        
    def change(self,direction,tense):
        if direction == 0:
            if tense == 0:
                content = ["increased" , "escalated" , "increased" , "rose" , "incremented"]
            elif tense == 1:
                if self.cat == "exaggerate":
                    content = content = ["increase" , "rise"]
                content = ["increase" , "growth" , "rise"]
            elif tense == 6:
                content = content = ["increase" , "rise", "grow"]
            else:
                content = ["increasing", "rising", "climbing", "escalating"]
        else:
            if tense == 0:
                content = ["declined" , "decreased" , "depleted" , "fell" , "reduced"]
            elif tense == 1:
                content = ["decrease" ,"fall" , "reduction"]
            elif tense == 6:
                content = ["decrease" ,"fall" , "reduce", "deplete"]
            else:
                content = ["decreasing", "falling", "reducing", "depleting", "declining"]
        a = random.choice(content)
        if self.previous_change == None:
            self.previous_change = a
            return(a)
        else:
            while a[:3] == self.previous_change[:3]:
                a = random.choice(content)
            self.previous_change = a
            return(a)
        
    def mm(self,val):
        if val == 0:
            return("maximum")
        else:
            return("minimum")   
    def constant(self):
        if len(self.additional) > 1:
            n1 = self.additional[0]
            n2 = self.additional[1]
            if self.state == 0:
                content = ["after",self.change(n1[0],2),"to a ", self.mm(n1[0]),"of", str(n1[1]), "on", n1[2], "and", self.change(n2[0],2)," to a ", self.mm(n2[0]),"of", str(n2[1]), "in", n2[2]]
            else:
                content = ["with",self.lb, "reaching its", self.mm(n1[0]), "value of $", str(n1[1]), "in", n1[2], "and", self.mm(n2[0]), "value of $", str(n2[1]), "in", n2[2]]
        else:
            n1 = self.additional[0]
            if self.state == 0:
                content = ["after",self.change(n1[0],2),"to a ", self.mm(n1[0]),"of $", str(n1[1]), "in", n1[2]]
            else:
                content = ["with",self.lb, "reaching its", self.mm(n1[0]), "value of $", str(n1[1]), "in", n1[2]]
        return(content)
    
    def exception(self):
        amplif = random.choice(["a sharp" ,"a steep" , "a sudden", "a"])
        content = [['except for',amplif,self.change(self.additional[0],1),"to $",str(self.additional[1]),"in",self.additional[2]],["although",self.lb,self.change(self.additional[0],0),"to $",str(self.additional[1]),"in",self.additional[2]],["despite",self.change(self.additional[0],2),"to $",str(self.additional[1]),"in",self.additional[2]]]
        return(random.choice(content))
    
    def exaggeration(self):
        def local_sent(node):
            sent = [self.change(self.changex,1),random.choice(["to $", "to a value of $"]),str(node[0]), "by" , node[1]]
            return(sent)
        amplif = random.choice(["a sharp" ,"a steep" , "a sudden"])
        content = ["During this period,",self.lb]
        for index, node in enumerate(self.additional):
            if index == len(self.additional)-1:
                content+=[" and further continued to"]
                content+=[self.change(self.changex,6),random.choice(["to $", "to a value of $"]),str(node[0][0]), "by" , node[0][1]]
            if index == 0:
                content+=[self.change(self.changex,0),"slightly ",random.choice(["to $", "to a value of $"]),str(node[0][0]), "by" , node[0][1], ","]
            if node[1] != None:
                content+=[', except for',amplif,self.change(node[1][0][0],1),"to $",str(node[1][0][1]),"in",node[1][0][2]]
        return(content)
                
    def step(self,series=False):
        def local_sent(node):
            sent = [self.change(self.changex,0),random.choice(["to $", "to a value of $"]),str(node[0]), "by" , node[1]]
            return(sent)
        content = ["During this period,",self.lb]
        content+=[self.change(self.additional[0][0],0),random.choice(["to $", "to a value of $"]),str(self.additional[0][1]), "by" , self.additional[0][2]]
        content+=[random.choice(["but immediately","but","but again"])]
        content+=[self.change(self.additional[1][0],0),"back",random.choice(["to $", "to a value of $"]),str(self.additional[1][1]), "by" , self.additional[1][2],"."]
        return(content)
        
            
        
                
                
            
    
                
                
            
            
    def gen_sent(self,param=None):
        content = [self.period(param)+[","]+self.gen_data(), self.gen_data()+self.period(param)]
        return(random.choice(content))
    def gen_data(self):
        if self.cat == "constant":
            self.state = 1
        self.state = random.randint(0,1)
        if self.state == 0:
            return([self.lb]+self.growth()+self.rang())
        else:
            return(["there was"]+self.growth()+self.rang())
                    
            
    def growth(self):
        def gfactor():
            if self.state == 1:
                if self.cat == "series":
                    content = ['an uneven', 'an irregular', 'a non-uniform', 'a jagged']
                elif self.grate == 1:
                    content = ["a sharp" ,"a steep" , "a sudden" , "an enormous" , "a"]
                elif self.grate == 2:
                    content = ["a significant", "a considerable", "a"]
                elif self.grate == 3:
                    if int(self.perc) > 100:
                        content = [""]
                    else:
                        content = ["a marginal", "a slight"]
            else:
                
                if self.cat == "series":
                    content = ['unevenly', 'irregularly', 'non-uniformly', 'jaggedly']
                elif self.grate == 1:
                    content = ["sharply" , "suddenly"]
                elif self.grate == 2:
                    content = ["significantly" , "considerably", ""]
                elif self.grate == 3:
                    if int(self.perc) > 100:
                        content = [""]
                    else:
                        content = ["marginally" , "slightly"]
            return(random.choice(content))
        if self.state == 1:
            return([gfactor(),self.change(self.changex,1)])
        else:
            content = [[gfactor(),self.change(self.changex,0)],[self.change(self.changex,0),gfactor()]]
            return(random.choice(content))
    

    def label_type(self):
        if self.lb == 0:
            content = ["it"]
        else:
            content = [self.label]
        return(random.choice(content))


    def rang(self):
        if self.state == 1:
            PY = "of"
        else:
            PY = "by"
        
        if (self.additional) != None and len(self.additional) > 1 and self.cat != "exception":
            content = [[PY,self.perc_type()]]
            if self.perc_type()[0] == "0":
                content = [[""]]
        else:
            content = [["from",self.X(),"to",self.Y()]]
        return(random.choice(content))
    def X(self):
        return("$"+str(self.iv))
    def Y(self):
        return("$"+str(self.fv))
    def perc_type(self):
        return(str(self.perc)+"%")
    def period(self,param):
        if param == None:
            content = [["during the period,",'\033[1m', self.SDATE(), "-", self.EDATE(),'\033[0m'] , ["between", '\033[1m', self.SDATE(), "&", self.EDATE(),'\033[0m'] , ["from", '\033[1m', self.SDATE(), "to", self.EDATE(),'\033[0m']]
        else:
            content = [["between", '\033[1m', self.SDATE(), "&", self.EDATE(),'\033[0m'] , ["from", '\033[1m', self.SDATE(), "to", self.EDATE(),'\033[0m']]
        return(random.choice(content))
    def SDATE(self):
        return(self.sdate)
    def EDATE(self):
        return(self.edate)


