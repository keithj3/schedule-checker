import datetime


class Schedule():
    
    '''
    Pass 3 datetime time objects. Beginning of schedule
    period (start_obj), end of schedule period (end_obj),
    and the time to check (check_obj).

    Will raise exception if start_obj == end_obj and return 
    false.

    Print inspect() to view in command line.
    '''

    def __init__(self, start_obj, end_obj, check_obj):
        
        self.start_obj = start_obj
        self.end_obj = end_obj
        self.check_obj = check_obj

        if not all(isinstance(i, datetime.time) for i in \
                            [self.start_obj, self.end_obj, self.check_obj]):
            raise TypeError('Must pass datetime.time object.')
        

    # If schedule crosses midnight.
    def get_mode(self):

        _s_int = int(str(self.start_obj.hour) + str(self.start_obj.minute))
        _e_int = int(str(self.end_obj.hour) + str(self.end_obj.minute))
        _c_int = int(str(self.check_obj.hour) + str(self.check_obj.minute))
        
        if (_e_int - _s_int) >= 0:
            return 'standard'
        else:
            return 'reverse'

    
    def is_in_schedule(self):

        if self.start_obj == self.end_obj:
            raise Exception('Returning out of schedule because start time == end time.')
            return False

        if self.get_mode() == 'standard':   
            return self.start_obj <= self.check_obj <= self.end_obj

        elif self.get_mode() == 'reverse':
            return ( ( self.check_obj >= self.start_obj ) or ( self.check_obj <= self.end_obj ) )

    def inspect(self):
        return 'start: {s} || check: {c} || end: {e} || In schedule: {isch} || mode: {m}\n'.format(\
                                s=str(self.start_obj), c=str(self.check_obj), \
                                e=self.end_obj, isch=self.is_in_schedule(), m=self.get_mode())







