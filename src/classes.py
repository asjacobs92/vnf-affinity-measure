class Criterion(object):
    def __init__(self, name, type, scope, formula):
        self.name = name
        self.type = type
        self.scope = scope
        self.formula = formula
        self.weight = 1
    
class VNF(object):
    def __init__(self, id, label, pm, fg, flavor, vm_cpu, vm_mem, vm_sto, cpu_usage, mem_usage, sto_usage):
        self.id = int(id)
        self.label = label
        self.pm = pm
        self.fg = fg
        self.flavor = flavor
        self.vm_cpu = float(vm_cpu)
        self.vm_mem = float(vm_mem)
        self.vm_sto = float(vm_sto)
        self.cpu_usage = float(cpu_usage)
        self.mem_usage = float(mem_usage)
        self.sto_usage = float(sto_usage)

class PM(object):
    def __init__(self, id, cpu, mem, sto):
        self.id = int(id)
        self.cpu = float(cpu) 
        self.mem = float(mem)
        self.sto = float(sto)
        
class FG(object):
    def __init__(self, id, flows):
        self.id = int(id)
        self.flows = flows
    
class Flow(object):
    def __init__(self, src, dst, lat, trf, bnd_usage, pkt_loss):
        self.src = int(src)
        self.dst = int(dst)
        self.lat = float(lat)
        self.trf = float(trf)
        self.bnd_usage = float(bnd_usage)
        self.pkt_loss = float(pkt_loss)
        
class Flavor(object):
    def __init__(self, id, min_cpu, min_mem, min_sto):
        self.id = int(id)
        self.min_cpu = float(min_cpu)
        self.min_mem = float(min_mem)
        self.min_sto = float(min_sto)

class NSD(object):
    def __init__(self, sla = 30.0, conflicts = []):
        self.sla = float(sla)
        self.conflicts = conflicts
