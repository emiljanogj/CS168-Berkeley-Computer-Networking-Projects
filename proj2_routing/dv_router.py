"""Your awesome Distance Vector router for CS 168."""

import sim.api as api
import sim.basics as basics

# We define infinity as a distance of 16.
INFINITY = 16


class DVRouter(basics.DVRouterBase):
    # NO_LOG = True # Set to True on an instance to disable its logging
    # POISON_MODE = True # Can override POISON_MODE here
    # DEFAULT_TIMER_INTERVAL = 5 # Can override this yourself for testing

    def __init__(self):
        """
        Called when the instance is initialized.

        You probably want to do some additional initialization here.

        """
        self.start_timer()  # Starts calling handle_timer() at correct rate

        self.table={} #for each node there will be a list of tuples. For example:[node1:[(port1,cost1),(port2,cost2),...(portk,costk)],node2:[(port1,cost1)..]]
        self.dv={}
        self.neigh={}
    
    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this Entity goes up.

        The port attached to the link and the link latency are passed
        in.

        """
        self.neigh[port]=latency
        self.table[port]={}
        for dest in self.dv:
            self.send(basics.RouterPacket(dest,self.dv[dest][0]),port)
        pass

    def handle_link_down(self, port):
        """
        Called by the framework when a link attached to this Entity does down.

        The port number used by the link is passed in.

        """
        self.neigh[port]=INFINITY
        self.table.pop(port)
        self.neigh.pop(port)
        for dest in self.dv:
            if self.dv[dest][1]==port:
                min_cost=INFINITY
                hop=None
                for pp in self.neigh:
                    entries=self.table[pp]
                    if dest in entries:
                        if min_cost > entries[dest][0]+self.neigh[pp]:
                            min_cost=entries[dest][0]+self.neigh[p]
                            next_hop=hop
                self.dv[dest]=(dest,next_hop)

            for pp in self.neigh:
                if pp==hop:
                    if self.POISON_MODE:
                        self.send(basics.RouterPacket(dest,INFINITY),pp)
                else:
                    if min_cost==INFINITY:
                        if self.POISON_MODE:
                            self.send(basics.RouterPacket(dest,INFINITY),pp)
                    else:
                        self.send(basics,RouterPacket(dest,self.dv[dest][0]),pp)
                
                        
        pass

    def handle_rx(self, packet, port):
        """
        Called by the framework when this Entity receives a packet.

        packet is a Packet (or subclass).
        port is the port number it arrived on.

        You definitely want to fill this in.

        """
        #self.log("RX %s on %s (%s)", packet, port, api.current_time())
        if isinstance(packet, basics.RoutePacket):

            self.table[port][packet.destination]=(packet.latency+self.neigh[port],api.current_time())
            dest=packet.destination
            if dest not in self.dv:    
                self.dv[dest]=(self.neigh[port]+packet.latency,port)
                for p in self.neigh:
                    if p==port:
                        if self.POISON_MODE:
                            self.send(basics.RoutePacket(dest,INFINITY),p)
                    else:
                        self.send(basics.RoutePacket(dest,packet.latency+self.neigh[port]),p)
            else:
                min_cost=INFINITY
                min_cost=self.dv[dest][0] if self.dv[dest][1]!=port else packet.latency + self.neigh[port]
                if packet.latency+self.neigh[port]<=min_cost:
                    min_cost=packet.latency+self.neigh[port]
                if self.dv[dest][0]!=min_cost:
                    self.dv[dest]=(min_cost,port)
                    for p in self.neigh:
                        if p==port:
                            if self.POISON_MODE:
                                self.send(basics.RoutePacket(dest,INFINITY),p)
                            else:
                                self.send(basics.RoutePacket(dest,min_cost),p)
                        else:
                            if min_cost==INFINITY:
                                if self.POISON_ROUTE:
                                    self.send(basics.RoutePacket(dest,INFINITY),p)
                            else:
                                self.send(basics.RoutePacket(dest,min_cost),p)
            
            
        elif isinstance(packet, basics.HostDiscoveryPacket):
            self.table.pop(port)
            self.neigh.pop(port)
            self.dv[packet.src]=(latency,port)
            for p in self.neigh:
                self.send(basics.RoutePacket(packet.src,latency),p)
        else:
            if packet.dst in self.dv:
                if self.dv[packet.dst][1]!=port:
                    self.send(packet,self.dv[packet.dst][1])
            
    def handle_timer(self):
        """
        Called periodically.

        When called, your router should send tables to neighbors.  It
        also might not be a bad place to check for whether any entries
        have expired.

        """
        for p in self.neigh:
            expired=[]
            for dest in self.table[p]:
                if api.current_time() - self.table[p][dest][1] >=15:
                    self.table[p][dest]=(INFINITY,api.current_time())
                    expired.append(p)
                    if self.dv[dest][1]==p:
                        min_cost=INFINITY
                        hop=None
                        for pp in self.neigh:
                            entities=self.table[p]
                            if dest in ent:
                                if ent[dest][0] + self.neigh[pp]<=min_cost:
                                    min_cost=ent[dest][0]+self.neigh[pp]
                                    hop=pp
                        self.dv[dest]=(min_cost,hop)
            for dest in expired:
                self.table.pop(dest)

        for p in self.neigh:
            for dest in self.dv:
                if self.dv[dest][1]==p:
                    if self.POISON_MODE:
                        self.send(basics.RoutePacket(dest,INFINITY),p)
                else:
                    if self.dv[dest][0]<INFINITY and self.POISON_ROUTE:
                        self.send(basics.RoutePacket(dest,self.dv[dest][0]),p)
                        
