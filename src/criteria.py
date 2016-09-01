from classes import Criterion, NSD

def min_cpu_affinity(vnf_a, vnf_b):
    if (vnf_a.vm_cpu >= vnf_a.flavor.min_cpu and vnf_b.vm_cpu >= vnf_b.flavor.min_cpu):
        return 1.0
    
    if (vnf_a.vm_cpu >= vnf_a.flavor.min_cpu and vnf_b.vm_cpu < vnf_b.flavor.min_cpu):
        return (1.0 + max(0.001, vnf_b.vm_cpu / vnf_b.flavor.min_cpu)) * 0.5
        
    if (vnf_a.vm_cpu < vnf_a.flavor.min_cpu and vnf_b.vm_cpu >= vnf_b.flavor.min_cpu):
        return (max(0.001, vnf_a.vm_cpu / vnf_a.flavor.min_cpu) + 1.0) * 0.5

    return (max(0.001, vnf_a.vm_cpu / vnf_a.flavor.min_cpu) + max(0, vnf_b.vm_cpu / vnf_b.flavor.min_cpu)) * 0.5


def min_mem_affinity(vnf_a, vnf_b):
    if (vnf_a.vm_mem >= vnf_a.flavor.min_mem and vnf_b.vm_mem >= vnf_b.flavor.min_mem):
        return 1.0
    
    if (vnf_a.vm_mem >= vnf_a.flavor.min_mem and vnf_b.vm_mem < vnf_b.flavor.min_mem):
        return (1.0 + max(0.001, vnf_b.vm_mem / vnf_b.flavor.min_mem)) * 0.5
        
    if (vnf_a.vm_mem < vnf_a.flavor.min_mem and vnf_b.vm_mem >= vnf_b.flavor.min_mem):
        return (max(0.001, vnf_a.vm_mem / vnf_a.flavor.min_mem) + 1.0) * 0.5

    return (max(0.001, vnf_a.vm_mem / vnf_a.flavor.min_mem) + max(0, vnf_b.vm_mem / vnf_b.flavor.min_mem)) * 0.5
    

def min_sto_affinity(vnf_a, vnf_b):
    if (vnf_a.vm_sto >= vnf_a.flavor.min_sto and vnf_b.vm_sto >= vnf_b.flavor.min_sto):
        return 1.0
    
    if (vnf_a.vm_sto >= vnf_a.flavor.min_sto and vnf_b.vm_sto < vnf_b.flavor.min_sto):
        return (1.0 + max(0.001, vnf_b.vm_sto / vnf_b.flavor.min_sto)) * 0.5
        
    if (vnf_a.vm_sto < vnf_a.flavor.min_sto and vnf_b.vm_sto >= vnf_b.flavor.min_sto):
        return (max(0.001, vnf_a.vm_sto / vnf_a.flavor.min_sto) + 1.0) * 0.5

    return (max(0.001, vnf_a.vm_sto / vnf_a.flavor.min_sto) + max(0, vnf_b.vm_sto / vnf_b.flavor.min_sto)) * 0.5
    

def conflicts_affinty(vnf_a, vnf_b):
    same_pm = (vnf_a.pm.id == vnf_b.pm.id)
    same_fg = (vnf_a.fg.id == vnf_b.fg.id)
    for conflict in nsd.conflicts:
        same_pm_conflict = (str(vnf_a.id) + ";" + str(vnf_b.id)) == conflict
        same_fg_conflict = (str(vnf_a.id) + "->" + str(vnf_b.id)) == conflict
        if ((same_pm_conflict and same_pm) or (same_fg_conflict and same_fg)):
            return 0.001;
    return 1.0
    

def cpu_usage_affinity(vnf_a, vnf_b):
    return max(0.001, 1.0 - ((vnf_a.cpu_usage + vnf_b.cpu_usage) / 100))
    
def mem_usage_affinity(vnf_a, vnf_b):
    return max(0.001, 1.0 - ((vnf_a.mem_usage + vnf_b.mem_usage) / 100))
    
def sto_usage_affinity(vnf_a, vnf_b):
    return max(0.001, 1.0 - ((vnf_a.sto_usage + vnf_b.sto_usage) / 100))
    
def bnd_usage_affinity(vnf_a, vnf_b):
    if (vnf_a.fg.id == vnf_b.fg.id):
        flow = next((x for x in vnf_a.fg.flows if ((x.src == vnf_a.id and x.dst == vnf_b.id) or (x.src == vnf_b.id and x.dst == vnf_a.id))), None)
        if (flow != None):
            return max(0.001, 1.0 - (flow.bnd_usage/100))
    return -1.0

def pkt_loss_affinity(vnf_a, vnf_b):
    if (vnf_a.fg.id == vnf_b.fg.id):
        flow = next((x for x in vnf_a.fg.flows if ((x.src == vnf_a.id and x.dst == vnf_b.id) or (x.src == vnf_b.id and x.dst == vnf_a.id))), None)
        if (flow != None):
            return max(0.001, 1.0 - (flow.pkt_loss/100))
    return -1.0

def lat_affinity(vnf_a, vnf_b):
    if (vnf_a.fg.id == vnf_b.fg.id):
        flow = next((x for x in vnf_a.fg.flows if ((x.src == vnf_a.id and x.dst == vnf_b.id) or (x.src == vnf_b.id and x.dst == vnf_a.id))), None)
        if (flow != None):
            return 1 if (2*flow.lat <= nsd.sla) else max(0.001, 1.0 - ((2*flow.lat - nsd.sla) / nsd.sla))
    return -1.0    

nsd = NSD()
criteria = [
    Criterion("min_cpu", "static", "pm", min_cpu_affinity),
    Criterion("min_mem", "static", "pm", min_mem_affinity),
    Criterion("min_sto", "static", "pm", min_sto_affinity),
    Criterion("conflicts", "static", "fg", conflicts_affinty),
    Criterion("cpu_usage", "dynamic", "pm", cpu_usage_affinity),
    Criterion("mem_usage", "dynamic", "pm", mem_usage_affinity),
    Criterion("sto_usage", "dynamic", "pm", sto_usage_affinity),
    Criterion("bnd_usage", "dynamic", "fg", bnd_usage_affinity),
    Criterion("pkt_loss", "dynamic", "fg", pkt_loss_affinity),
    Criterion("lat", "dynamic", "fg", lat_affinity)
]
