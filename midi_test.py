import rtmidi

midi_in = rtmidi.MidiIn()

print(midi_in.get_ports())

midi_device = int(input("Select device (Starting index 0)"))

try:
    midi_in.open_port(midi_device)
except Exception as e:
    print(e)
    #print("no midi instruments detected")


if midi_in.is_port_open():
    print("port open")
    
    while True:
        #get latest midi
        msg_and_t = midi_in.get_message()
        
        #if there is a message get the values
        if msg_and_t:
            (msg, dt) = msg_and_t
            channel = hex(msg[0])
            print(msg_and_t)
            
        

