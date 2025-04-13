class Env:
    
    def __init__(self, a, d, s, r):
        self.a_t = a
        self.d_t = d
        self.s_l = s
        self.r_t = r
        self.d_m = (s - 1)/d
        
    def apply(self, note, current_time):
        gain = 0
        
        #get time
        time_note_pressed = current_time - note.time_set
        
        if note.pressed:
            #attack
            if time_note_pressed <= self.a_t:
                gain = time_note_pressed/self.a_t
            
            #decay
            elif time_note_pressed <= self.a_t + self.d_t:
                gain = self.d_m * (time_note_pressed - self.a_t) + 1
                
            #sustain
            else:
                gain = self.s_l
            
            #set release slope and last gain
            note.last_gain = gain
            note.r_m = (0 - note.last_gain)/self.r_t
            
            #release    
        else:
            gain = note.r_m * (time_note_pressed/self.r_t) + note.last_gain
           
        return gain
        