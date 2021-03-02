
from mininet.topo import Topo
class tests(Topo):
    def __init__(self):
        Topo.__init__(self)
        #host
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        #switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        #switch and host
        self.addLink(h1,s1)
        self.addLink(h2,s2)
        self.addLink(h3,s3)
        self.addLink(h4,s4)
        self.addLink(s1,s2)
        self.addLink(s2,s3)
        self.addLink(s3,s4)

topos = {'mytopo':(lambda:tests())}

#self.addLink(h5,s1)
#self.addLink(h6,s2)
#self.addLink(h7,s3)
#self.addLink(h8,s4)

#self.addLink(h5,s5)
#self.addLink(h6,s6)
#self.addLink(h7,s7)
#self.addLink(h8,s8)

#switch and switch
#linkopts = dict(bw=1,loss=1,delay='1ms', max_queue_size=100,use_htb=True)
#self.addLink(s1, s2,**linkopts)
# self.addLink(s1,s2)
