# clean this f-in GFF
import os, sys

input_gff_file = sys.argv[1]
input_gff = open(input_gff_file, 'r')
output_gff_file = input_gff_file.replace(".gff", ".clean.gff")
output_gff = open(output_gff_file, 'w')

# possible lines starting with #:
# - ###
# - ##FASTA
# - ##gff-version 3

def process_gene_name(l):
    #print("l is {}, get it".format(l))
    l = l.strip().split("\t")
    print("l is {}, get it".format(l))
    if l[1] == "maker" and l[2] in ["gene", "mRNA"] and "Note=Similar to" in l[-1]:
        attributes = l[-1].strip(";").split(";")
        print("attributes are {}, get it".format(attributes))
        new_attributes_dict = {}
        for attribute in attributes:
            try:
                k, v = attribute.split("=")
                new_attributes_dict[k] = v
            except:
                sys.exit(attribute)
        gene_name = new_attributes_dict["Note"].split("Similar to")[1].strip().split(":")[0]
        if gene_name:
            print("Gene name: {}".format(gene_name))
            new_attributes_dict["Alias"] = new_attributes_dict["Alias"] + "," + gene_name
        print(new_attributes_dict)
        new_attributes = ""
        for k in new_attributes_dict:
            new_attributes += "{k}={v};".format(k=k, v=new_attributes_dict[k])
        l = "\t".join(l[:-1] + [new_attributes])
    else:
        l = "\t".join(l)
    return l
    
for l in input_gff:
    if l.startswith('#'):
        if "FASTA" not in l:
            output_gff.write(l)
    else:
        # trash non-gff lines
        if len(l.split('\t')) == 9:
            # add gene names to alias, if present
            l = process_gene_name(l)
            #type(l)
            output_gff.write(l + "\n")

output_gff.close()