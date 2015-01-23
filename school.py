from sys import argv
import math
import time
script, file = argv
start = time.time()
entity_demands = {}

heat = 0
demand_file = open(file)

for line in demand_file.readlines():
	k, v = line.split('=')
	entity_demands[k.strip()] = v.strip()

### taking demands off of list and making them into variables ####
class_meter_squared = int(entity_demands.pop('class_demensions'))
total_meter_squared = int(entity_demands.pop('outside_demensions'))
heat_amount = int(entity_demands.pop('heat'))
panel_voltage = int(entity_demands.pop('voltage'))
panel_phase = int(entity_demands.pop('phase'))
parallel_count = int(entity_demands.pop('parallel'))
equipment = entity_demands.pop('equipment')
wiring_method = entity_demands.pop('wiring_method')

sub = {}

	
def class_area_demand(x):
	c_demand = 50 * x
	sub['classroom'] = c_demand
	
def rest_of_area_demand(total_area, class_protion):
	hallways = total_area - class_protion
	hallway_demand = 10 * hallways
	sub['rest'] = hallway_demand
	
def space_heat_demand(x):
	if x > 0:
		heat_demand = 0.75 * x
		return heat_demand
	else:
		return 0

def check_parking():
	if 'parking_stalls' in entity_demands and 'restricted' in entity_demands:
		parking_demand(int(entity_demands.pop('parking_stalls')), entity_demands.pop('restricted'))
	else:
		parking_demand(int(entity_demands.pop('parking_stalls')), 'no')


		
def parking_demand(parking_stalls, restricted):
	sum = 0
	if restricted == 'yes':
		if parking_stalls > 60:
			sum = parking_stalls - 60
			x = 450.0 * all_over
			y = 550.0 * 30
			z = 650.0 * 30
			sum_large = x + y + z
		elif parking_stalls > 30 and parking_stalls < 60:
			sum = parking_stalls - 30
			x = 550.0 * parking_stalls
			y = 650.0 * 30
			sum_med = x + y
		else:
			sum = 650.0 * parking_stalls
	else:
		if parking_stalls > 60:
			sum = parking_stalls - 60
			x = 800.0 * all_over
			y = 1000.0 * 30
			z = 1200.0 * 30
			sum_large = x + y + z
		elif parking_stalls > 30 and parking_stalls < 60:
			sum = parking_stalls - 30
			x = 1000.0 * parking_stalls
			y = 1200.0 * 30
			sum_med = x + y
		else:
			sum = 1200.0 * parking_stalls
	sub['park'] = sum

	
	
### After taking the other loads off the dict I then iterate over the rest and add them up #####
def other_loads():
	sum = 0
	for k, v in entity_demands.items():
		sum += int(v)
	sub['other'] = sum
	
def per_square_meter(total, x_meters):
	watt_per_square = round(total / x_meters, 2)
	print watt_per_square,"Watts/meter"
	return watt_per_square
	
def subtotal():
	amount = 0
	for k, v in sub.items():
		amount += v
	print "Subtotal: %r Watts" % amount
	return amount
		

def calculated_wattage(wms, ad, heating):
	wattage_calculated = 0
	if ad < 900:
		wattage_calculated = round((wms * sd) * 0.75, 2)
		wattage_calculated = wattage_calculated + heating
	else:
		wattage_calculated_a = round((wms * 900) * 0.75, 2)
		wattage_calculated_b = round((wms * (ad - 900)) * 0.50,)
		wattage_calculated = wattage_calculated_a + wattage_calculated_b + heating
	print "Calculated wattage: %r WATTS" % wattage_calculated
	return wattage_calculated
	
def base_ampacity(volts, phases, watts):
	base_amp = 0
	if phases == 3:
		base_amp = round(watts / (math.sqrt(3) * volts), 1)
	else:
		base_amp = round((watts / volts), 1)
	print base_amp
	return base_amp
	
def min_ampacity(equip_type, wiring_style, x_base_amps):
	min_amp_amount = 0
	if equip_type == '100%' and wiring_style == 'conduit':
		min_amp_amount = x_base_amps
	elif equip_type == '100%' and wiring_style == "free_air":
		min_amp_amount = round(x_base_amps / 0.85, 1)
	elif equip_type == '80%' and wiring_method == 'free_air':
		min_amp_amount = round(x_base_amps / 0.70, 1)
	else:
		min_amp_amount = round(x_base_amps / 0.80, 1)
	print "Minimun circuit ampacity based on wiring method: %r A" % min_amp_amount
	return min_amp_amount
	

#### Calling my functions with above variables #####
class_area_demand(class_meter_squared)
rest_of_area_demand(total_meter_squared, class_meter_squared)
heat = space_heat_demand(heat_amount)
check_parking()
other_loads()
print sub
watt_sub = subtotal()
watts_per = per_square_meter(watt_sub, total_meter_squared)
base_watt = calculated_wattage(watts_per, total_meter_squared, heat)
calculated_amp = base_ampacity(panel_voltage, panel_phase, base_watt)
final_ampacity = min_ampacity(equipment, wiring_method, calculated_amp)
parallel_ampacity = round(final_ampacity / parallel_count, 1)
print "Therefore I need a conductor good for %r Amps while running %r parallel runs, for a main ampacity of %r Amps" % (parallel_ampacity, parallel_count, final_ampacity)

end = time.time() - start
print "Time for calculations: %r" % end