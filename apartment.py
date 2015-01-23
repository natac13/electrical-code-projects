# Import math was to use ceil
from __future__ import division
import math
from sys import argv

# I had to define this dict before calling any method that utilizes it.
demand_totals = {}

######### This is how I get the info from a txt file that I pass with the running of the script
entity_demands = {}
#### entity_demands will be my inputs in the form of a dict

script, file = argv
input_file = open(file)
## .readlines() will produce a list (array) of variables of the entire file with each line being an object in the list
## this make it perfect to iterate over with for loops
## .readline() is different and only reads a character at a time
## .xreadlines() will read one line at a time, therefore use this with really big file where I don't want to eat up memory
## more info  	http://www.peterbe.com/plog/blogitem-040312-1 #########
input_file_demands = input_file.readlines()
for x in input_file_demands:
	k, v = x.split("=")
	## The strip will remove the hidden \n new line, and spaces which would transfer with the value 
	entity_demands[k.strip()] = v.strip()



#### I could have the program execute over the info, and even out then to a file!!
#### This file then can be formatted to have a standard output that will give all the values I need in a nice display


#########Use HTML to get the input from user and to start the python program if possible
########## then at the end of the python program have it output to a file maybe even HTML

########## Need to put code rule for each function great way for me to learn them ###################

def min_wire_ampacity(wattage, voltage, phase):
	"""Will return the min wire ampacity by passing a wattage, voltage and phase of panel."""
	""" Does not account if the load is continuous."""
	if phase == 1:
		amp = wattage / voltage
	else:
		amp = wattage / (voltage * math.sqrt(3))
		
	ampacity_rounded = round(amp, 2)
	demand_totals['min_ampacity'] = ampacity_rounded
	print demand_totals
	print "The total unit demand is:",demand_totals['total_suit'],"Watts",
	print "and the subtotal is:", demand_totals['subtotal'], "Watts"
	print "The minimum wire and panel ampacity is: %r Amps" % ampacity_rounded


def suit_total_demand():
	suit_demand = demand_totals['heatna/c'] + demand_totals['subtotal']
	demand_totals['total_suit'] = suit_demand
	return suit_demand


def heat_ac(heat, ac):	
	if heat > ac:
		choose = 'heat'
	else:
		choose = 'ac'	
	if choose == "heat":
		heat_load = heat
		if heat_load <= 10000.0:
			demand_totals['heatna/c'] = heat_load
		else:
			heat_load_extra = .75 * (heat_load - 10000.0)
			total_heat = heat_load_extra + 10000.0
			demand_totals['heatna/c'] = total_heat
	else:
		ac_load = ac
		demand_totals['heatna/c'] = ac_load
		
	
def subtotal ():
	subtotal = 0.0
	for k, v in demand_totals.items():
		subtotal = subtotal + v
	# print "Your subtotal is:", subtotal,"Watts"
	demand_totals['subtotal'] = subtotal
	
	
def extra_loads(x):
	if x > 1500:
		extra_load_demand = x * 0.25
		demand_totals['extra'] = extra_load_demand
	else:
		demand_totals['extra'] = 0.0 
	
		# how do i add different things in the same loop to a dict, meaning a different 
		# KEY, value pair where the key keeps changing..... Something like item1:800, item2:856, item3:876
		# where the values are meaningless in what I am asking
		
		# or I should just ask for all the loads then have the function add them and take 25% of that like the code really says!
		

def range(x):
	if x <= 12000.0:
		demand_totals['range'] = 6000.0
	else:
		left_over = x - 12000.0
		downgraded = left_over * 0.4
		total = 6000.0 + downgraded
		demand_totals['range'] = total	
		
		
############ Rule: 8-202?        ############	
def area(x):
	"""Rule: 8-202"""
	if x <= 45:
		demand_totals['area'] = 3500.0
	elif x > 45 and x <= 90:
		demand_totals['area'] = 5000.0
	else:		
		# This ceil function round the number up so that I account for any addition 90m portion
		multi = math.ceil((x - 90) / 90.0)
		if multi > 1.0: 
			additional_wattage = 1000.0 * multi
			total_area_demand = 5000.0 + additional_wattage
			demand_totals['area'] = total_area_demand			
		else: 
			demand_totals['area'] = 6000.0			
		
			
# START		
def start():	
	area(int(entity_demands['area']))
	range(int(entity_demands['range']))
	extra_loads(int(entity_demands['extra_load']))
	subtotal()
	heat_ac(int(entity_demands['heat']), int(entity_demands['ac']))
	suit_total_demand()
	min_wire_ampacity(suit_total_demand(),int(entity_demands['suite_voltage']), int(entity_demands['suite_phase']))
	
	
start()
input_file.close()


