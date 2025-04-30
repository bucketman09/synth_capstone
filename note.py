class Note:
    def __init__(self, value, velocity, time_set, pressed, channel, last_gain = 0, r_m = 0):
        self.value = value
        self.velocity = velocity
        self.time_set = time_set
        self.pressed = pressed
        self.last_gain = last_gain