from classes import *

def parse_sla(data):
    return data["sla"]

def parse_conflicts(data):
    return data["conflicts"]
    
def parse_weight(data, criterion_name):
    try:
        return int(data["weights"][criterion_name])
    except:
        return 1

def parse_pms(data):
    pms = []
    for pm_data in data["pms"]:
        pm = PM(pm_data["id"], pm_data["cpu"], pm_data["mem"], pm_data["sto"])
        pms.append(pm)
    return pms

def parse_fg(data):
    flows = []
    for flow_data in data["flows"]:
        flow = Flow(flow_data["src"], flow_data["dst"], flow_data["lat"], flow_data["trf"], flow_data["bnd_usage"], flow_data["pkt_loss"])
        flows.append(flow)
    fg = FG(data["id"], flows)
    return fg

def parse_flavors(data):
    flavors = []
    for flavor_data in data["flavors"]:
        flavor = Flavor(flavor_data["id"], flavor_data["min_cpu"], flavor_data["min_mem"], flavor_data["min_sto"])
        flavors.append(flavor)
    return flavors

def parse_vnfs(data, pms, fgs, flavors):
    vnfs = []
    for vnf_data in data["vnfs"]:
        vnf_pm = next((x for x in pms if x.id == int(vnf_data["pm"])), None)
        vnf_flavor = next((x for x in flavors if x.id == int(vnf_data["flavor"])), None)
        vnf_fgs = []
        for vnf_fg in vnf_data["fgs"]:
            vnf_fgs.append(next((x for x in fgs if x.id == int(vnf_fg)), None))
        vnf = VNF(vnf_data["id"], vnf_data["label"], vnf_pm, vnf_fgs, vnf_flavor, vnf_data["vm_cpu"], vnf_data["vm_mem"], vnf_data["vm_sto"], vnf_data["cpu_usage"], vnf_data["mem_usage"], vnf_data["sto_usage"])
        vnfs.append(vnf)  
    return vnfs
