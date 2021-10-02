import collections
from collections import Counter
import operator
import glob
import csv

#Import the predeveloped dictionary (provided in the repository)

with open('combined_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    mydict = {rows[0]:rows[1] for rows in reader}
    
#Import all the bills in .txt format, create a list of bill text

import zipfile
with zipfile.ZipFile('_all_proposed_bills.zip', 'r') as zip_ref:
        zip_ref.extractall()
list_all = glob.glob('*.txt')

#check the bill list

print(list_all)

#Check the keys for each bill
for file in list_all:
    ifile = open(file, 'r', encoding="utf8", errors='ignore').read()
    b = []
    for key in mydict:
        if key in ifile:
            b.append(mydict[key])
    print(b)

#Count the keys for each bill
alist = []
for file in list_all:
    ifile = open(file, 'r', encoding="utf8", errors='ignore').read()
    c = []
    for key in mydict:
        if key in ifile:
            c.append(mydict[key])
    cnt_c = Counter(c)
    alist.append(cnt_c)

#Check the list of key objects in each bill. The list should look like: 
#[Counter({'rule_authority': 10, 'object_ogdevelopment': 7, 'rule_info': 7, 'rule_choice': 6, 'object_resource': 5, 'object_policies_other': 4, 
#'object_envir_health': 4, 'rule_enforcement': 4, 'rule_deontic_must': 4, 'object_tax_finance': 2, 'object_og_policies_strategies': 2, 
#'rule_constitutive': 2, 'actor_court': 1, 'actor_expert': 1, 'actor_industry': 1, 'actor_other': 1, 'actor_state': 1, 'rule_deontic_may': 1, 
#'rule_position': 1}), Counter({'rule_info': 34,...})], with the number of counter objects equal the number of bills.

#convert counter objects to lists, create a list of all lists

freq_list = [list(y.items()) for y in alist]
freq_conv = [list(x) for x in freq_list]
print(freq_conv)

#The list should look like:
#[[('actor_court', 1), ('actor_expert', 1), ('actor_industry', 1), ('actor_other', 1), ('actor_state', 1), ('object_tax_finance', 2), 
#('object_ogdevelopment', 7), ('object_og_policies_strategies', 2), ('object_policies_other', 4), ('object_envir_health', 4), 
#('object_resource', 5), ('rule_info', 7), ('rule_enforcement', 4), ('rule_authority', 10), ('rule_choice', 6), ('rule_constitutive', 2), 
#('rule_deontic_may', 1), ('rule_deontic_must', 4), ('rule_position', 1)], [()...()], [()...()]]

#Combine bill names and the lists of terms 

tuple_name = []
for bills in list_all:
    bills = tuple([bills])
    tuple_name.append(bills)
#This list should look like: [('CO_SB165_P.txt',), ('ND_HB1026_P.txt',), ('CO_HB1379_P.txt',)...]

combined = list(zip(tuple_name, freq_conv))
#This list should look like: 
#[(('CO_SB165_P.txt',), [('actor_court', 1), ('actor_expert', 1), ('actor_industry', 1), ('actor_other', 1), ('actor_state', 1), 
#('object_tax_finance', 2), ('object_ogdevelopment', 7), ('object_og_policies_strategies', 2), ('object_policies_other', 4), ('object_envir_health', 4), 
#('object_resource', 5), ('rule_info', 7), ('rule_enforcement', 4), ('rule_authority', 10), ('rule_choice', 6), ('rule_constitutive', 2), 
#('rule_deontic_may', 1), ('rule_deontic_must', 4), ('rule_position', 1)]), (('ND_HB1026_P.txt',)[()...()])]

#Define a function to flatten the list

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list
    
    
#Flatten the list "combined" such that each bill-sublist contain only tuples

combined_delist = []
for lists in combined:
    combined_delist.append(flatten_list(lists))    
 
combined_db_delist = flatten_list(combined_delist) 

#Export analysis results
import csv

with open('combined_analysis.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['category','count'])
    for row in combined_db_delist:
        csv_out.writerow(row)

#An example of results can be found in the repository ("combined_analysis.csv")
