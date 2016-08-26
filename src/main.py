import json, xlwt
from math import *
from parser import *
from criteria import *
from affinity import *

with open("../input/input.json") as data_file:
    data = json.load(data_file)
    data_file.close()

pms = parse_pms(data)
fgs = parse_fgs(data)
flavors = parse_flavors(data)
vnfs = parse_vnfs(data, pms, fgs, flavors)

nsd.sla = parse_sla(data)
nsd.conflicts = parse_conflicts(data)
for criterion in criteria:
    criterion.weight = parse_weight(data, criterion.name)

book = xlwt.Workbook(encoding="utf-8")
sheet = book.add_sheet("affinity")

row_offset = 0
for i in range(0, len(vnfs)):
    for j in range(i + 1, len(vnfs)):
        sheet.write_merge(row_offset, row_offset, 0, 8, "VNF: " + str(vnfs[i].label))
        sheet.write_merge(row_offset, row_offset, 9,  17, "VNF: " + str(vnfs[j].label))
        sheet.write_merge(row_offset, row_offset, 18,  21, "FG")
        sheet.write_merge(row_offset, row_offset, 22,  30, "Affinity")
        
        """ headers """
        row = row_offset + 1
        sheet.write(row, 0, "min cpu")
        sheet.write(row, 1, "min mem")
        sheet.write(row, 2, "min sto")
        sheet.write(row, 3, "vm cpu")
        sheet.write(row, 4, "vm mem")
        sheet.write(row, 5, "vm sto")
        sheet.write(row, 6, "cpu usage")
        sheet.write(row, 7, "mem usage")
        sheet.write(row, 8, "sto usage")
        sheet.write(row, 9, "min cpu")
        sheet.write(row, 10, "min mem")
        sheet.write(row, 11, "min sto")
        sheet.write(row, 12, "vm cpu")
        sheet.write(row, 13, "vm mem")
        sheet.write(row, 14, "vm sto")
        sheet.write(row, 15, "cpu usage")
        sheet.write(row, 16, "mem usage")
        sheet.write(row, 17, "sto usage")
        sheet.write(row, 18, "bnd usage")
        sheet.write(row, 19, "pkt loss")
        sheet.write(row, 20, "lat")
        sheet.write(row, 21, "trf")
        sheet.write(row, 22, "trf aff")
        sheet.write(row, 23, "static pm aff")
        sheet.write(row, 24, "static fg aff")
        sheet.write(row, 25, "dynamic pm aff")
        sheet.write(row, 26, "dynamic fg aff")
        sheet.write(row, 27, "network aff")
        sheet.write(row, 28, "static aff")
        sheet.write(row, 29, "dynamic aff")
        sheet.write(row, 30, "aff")

        """ values """
        row += 1
        sheet.write(row, 0, vnfs[i].flavor.min_cpu)
        sheet.write(row, 1, vnfs[i].flavor.min_mem)
        sheet.write(row, 2, vnfs[i].flavor.min_sto)
        sheet.write(row, 3, vnfs[i].vm_cpu)
        sheet.write(row, 4, vnfs[i].vm_mem)
        sheet.write(row, 5, vnfs[i].vm_sto)
        sheet.write(row, 6, vnfs[i].cpu_usage)
        sheet.write(row, 7, vnfs[i].mem_usage)
        sheet.write(row, 8, vnfs[i].sto_usage)
        sheet.write(row, 9, vnfs[j].flavor.min_cpu)
        sheet.write(row, 10, vnfs[j].flavor.min_mem)
        sheet.write(row, 11, vnfs[j].flavor.min_sto)
        sheet.write(row, 12, vnfs[j].vm_cpu)
        sheet.write(row, 13, vnfs[j].vm_mem)
        sheet.write(row, 14, vnfs[j].vm_sto)
        sheet.write(row, 15, vnfs[j].cpu_usage)
        sheet.write(row, 16, vnfs[j].mem_usage)
        sheet.write(row, 17, vnfs[j].sto_usage)
        
        if (vnfs[i].fg.id == vnfs[j].fg.id):
            flow = next((x for x in vnfs[i].fg.flows if ((x.src == vnfs[i].id and x.dst == vnfs[j].id) or (x.src == vnfs[j].id and x.dst == vnfs[i].id))), None)
            if (flow != None):
                sheet.write(row, 18, flow.bnd_usage)
                sheet.write(row, 19, flow.pkt_loss)
                sheet.write(row, 20, flow.lat)
                sheet.write(row, 21, flow.trf)
                
        sheet.write(row, 22, trf_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 23, static_pm_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 24, static_fg_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 25, dynamic_pm_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 26, dynamic_fg_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 27, network_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 28, static_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 29, dynamic_affinity(vnfs[i], vnfs[j]))
        sheet.write(row, 30, affinity(vnfs[i], vnfs[j]))
        
        book.save("../output/affinity.xls")
        row_offset += 5
    




    
    
    

    