import pytest
import datetime
from datetime import time as time
import random

from time_functions import Schedule


def t_obj(h, m):
	return time(h, m)


wrong_objects = (
				(t_obj(8, 0), datetime.datetime(2019, 1, 16, 8, 8, 8), t_obj(12, 0)),
				(datetime.datetime(2019, 8, 8, 8, 8, 8), t_obj(8, 0), t_obj(9, 0)),
				('08:00', t_obj(12, 0), t_obj(9, 0)),
				)


def create_sets(in_schedule=True, reverse=False):
	
	'''
	To test in-schedule tuples of (starttime, endtime, timetocheck),
	pass in_schedule=True. in_schedule=False will test out-of-schedule
	timetocheck.

	To represent schedules that cross midnight (8PM to 4AM), 
	pass reverse=True
	'''
	
	_sets = []
	
	for i in (1, 2, 4, 6, 7, 11, 12, 13, 20, 21, 22):
		for x in (1, 30, 50, 57):

			start = t_obj(i, x)
	
			if reverse:
				_end_hour = i - random.randint(1, 20) 
				if _end_hour < 0:
					_end_hour = 0

				end = t_obj(_end_hour, x)
			
			else:
				end = t_obj( ( min(i+random.randint(1, 20), 23)), x )

			if reverse:
				
				if in_schedule:
					c_hour = random.randint(0, end.hour)

				else:
					c_hour = random.randint(end.hour, start.hour)

			else:
				
				if in_schedule:
					c_hour = random.randint(start.hour, end.hour)

				else:
					_before = random.randint(0, start.hour)
					_after = random.randint(end.hour, 23)
					c_hour = random.choice([_before, _after])
	
			if c_hour == start.hour:

				if in_schedule:
					c_min_min = start.minute + 1
					c_max_min = 58

				else:
					c_min_min = 0
					c_max_min = start.minute - 1
				
			elif c_hour == end.hour:
				
				if in_schedule:
					c_min_min = 0
					c_max_min = end.minute - 1

				else:
					c_min_min = end.minute + 1
					c_max_min = 59
			
			else:
				c_max_min = 59
				c_min_min = 0

			check = t_obj(c_hour, random.randint(c_min_min, c_max_min))

			_sets.append((start, end, check))

	edge_cases_standard = [
					(t_obj(0,0), t_obj(0,1), t_obj(0,1)),
					(t_obj(0,0), t_obj(0,1), t_obj(0,0)),
					(t_obj(23,58), t_obj(23,59), t_obj(23,58)),
					(t_obj(23,58), t_obj(23,59), t_obj(23,59)),
					(t_obj(13,0), t_obj(14,0), t_obj(13,0)),
					(t_obj(13,0), t_obj(14,0), t_obj(14,0)),
				 		  ]

	edge_cases_reverse = [
					(t_obj(0,1), t_obj(0,0), t_obj(0,0)),
					(t_obj(0,1), t_obj(0,0), t_obj(0,1)),
					(t_obj(23,59), t_obj(0,0), t_obj(0,0)),
					(t_obj(23,59), t_obj(0,0), t_obj(23,59)),
						 ]
	
	if in_schedule:
	
		if reverse:
			final_return = _sets + edge_cases_reverse
		else:
			final_return = _sets + edge_cases_standard
	
	else:

		final_return = _sets

	return final_return
	

def test_Schedule():

	# Does reject non-time-objs?
	for _set in wrong_objects:
		with pytest.raises(TypeError):
			s = Schedule(_set[0], _set[1], _set[2])
			assert s

	# Does return exception when start time = end time?
	_set = (t_obj(0,0), t_obj(0,0), t_obj(0,0))
	
	with pytest.raises(Exception):
		
		s = Schedule(t_obj(0,0), t_obj(0,0), t_obj(0,0))
		assert s.is_in_schedule() == False
		
		s = Schedule(t_obj(12,30), t_obj(12,30), t_obj(4,0))
		assert s.is_in_schedule() == False

	
	# IN SCHEDULE

	for _set in create_sets():

		# Does set mode == standard if start < end (does not cross midnight)?
		s = Schedule(_set[0], _set[1], _set[2])
		assert s.get_mode() == 'standard'

		# Does correctly place in schedule?
		assert s.is_in_schedule() == True

	
	# Schedules that cross midnight
	for _set in create_sets(reverse=True):

		# Does set mode == reverse if end < start?
		s = Schedule(_set[0], _set[1], _set[2])
		assert s.get_mode() == 'reverse'

		# Does correctly place in schedule?
		assert s.is_in_schedule() == True

	
	# OUT OF SCHEDULE

	for _set in create_sets(in_schedule=False):

		# Does set mode == standard if start < end?
		s = Schedule(_set[0], _set[1], _set[2])
		assert s.get_mode() == 'standard'

	# Schedules that cross midnight
	for _set in create_sets(in_schedule=False, reverse=True):
		
		# Does set mode == reverse if end < start?
		s = Schedule(_set[0], _set[1], _set[2])
		assert s.get_mode() == 'reverse'

		# Does correctly place out of schedule?
		assert s.is_in_schedule() == False




