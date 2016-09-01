from classes import *
from criteria import *

def criteria_affinity(vnf_a, vnf_b, type, scope):
    filtered_criteria = (x for x in criteria if x.type == type and x.scope == scope)
    weights_sum = 0
    affinities_sum = 0
    for criterion in filtered_criteria:
        weights_sum += criterion.weight
        affinities_sum += 1.0/criterion.formula(vnf_a, vnf_b)
    return weights_sum/affinities_sum

def static_pm_affinity(vnf_a, vnf_b):
    return criteria_affinity(vnf_a, vnf_b, "static", "pm")

def static_fg_affinity(vnf_a, vnf_b):
    return criteria_affinity(vnf_a, vnf_b, "static", "fg")

def dynamic_pm_affinity(vnf_a, vnf_b):
    return criteria_affinity(vnf_a, vnf_b, "dynamic", "pm")
    
def dynamic_fg_affinity(vnf_a, vnf_b):
    return criteria_affinity(vnf_a, vnf_b, "dynamic", "fg")
    
def static_affinity(vnf_a, vnf_b):
    static_pm_aff = static_pm_affinity(vnf_a, vnf_b)
    static_fg_aff = static_fg_affinity(vnf_a, vnf_b)
    return 2.0 / ((1/static_pm_aff) + (1/static_fg_aff))
    
def trf_affinity(vnf_a, vnf_b):
    vnf_a_fgs_ids = set(x.id for x in vnf_a.fgs)
    vnfs_fgs = [fg for fg in vnf_b.fgs if fg.id in vnf_a_fgs_ids]
    
    vnfs_trf = 0
    max_fg_trf = 0
    for fg in vnfs_fgs:
        for flow in fg.flows:
            if ((flow.src == vnf_a.id and flow.dst == vnf_b.id) or (flow.src == vnf_b.id and flow.dst == vnf_a.id)):
                vnfs_trf += flow.trf
            if (flow.trf > max_fg_trf):
                max_fg_trf = flow.trf
                
    return max(0.001, float(vnfs_trf)/max_fg_trf) if (vnfs_trf != 0) else -1.0
    
def network_affinity(vnf_a, vnf_b):
    trf_aff = trf_affinity(vnf_a, vnf_b)
    dynamic_fg_aff = dynamic_fg_affinity(vnf_a, vnf_b)
    return max(0.001, 0.5 + ((trf_aff/2.0) * float(dynamic_fg_aff - (1.0 - dynamic_fg_aff))))

def dynamic_affinity(vnf_a, vnf_b):
    x = 1 if (vnf_a.pm.id == vnf_b.pm.id) else 0
    y = 1 if (next((x for x in vnf_a.fg.flows if ((x.src == vnf_a.id and x.dst == vnf_b.id) or (x.src == vnf_b.id and x.dst == vnf_a.id))), None) != None) else 0
    if (x == 0 and y == 0):
        return 1.0

    dynamic_pm_aff = dynamic_pm_affinity(vnf_a, vnf_b)
    network_aff = network_affinity(vnf_a, vnf_b)
    return (x + y) / ((x/dynamic_pm_aff) + (y/network_aff))
    
def affinity(vnf_a, vnf_b):
    static_aff = static_affinity(vnf_a, vnf_b)
    w = 1 if (vnf_a.cpu_usage != 0 or vnf_b.cpu_usage != 0) else 0
    if (w == 0):
        return static_aff
    
    dynamic_aff = dynamic_affinity(vnf_a, vnf_b)
    return 2.0 / ((1.0/static_aff) + (w/dynamic_aff))