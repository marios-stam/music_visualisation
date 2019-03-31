import pyaudio # from http://people.csail.mit.edu/hubert/pyaud
import numpy  as np # from http://numpy.scipy.org/
import audioop
import sys
import math
import struct
import serial,time

'''
Sources
http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2
'''

MAX = 0
arduino = serial.Serial('COM3', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio() 
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print (str(i)+'. '+dev['name'])
        i += 1

def arduino_soundlight(): 
    chunk      = 2**11 # Change if too fast/slow, never less than 2**11
    scale      = 50    # Change if too dim/bright
    exponent   = 5    # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100 
    device   = 1  
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
    print ("Starting, use Ctrl+C to stop")
    try:
        current_level=0
        while True:
            data  = stream.read(chunk)
           
            newValue=amplitude_analysis(data,scale,exponent)
            current_level+= int ( (newValue-current_level)/4)
            #current_level=newValue
            print("#"* current_level )
            send_int_to_arduino(current_level)
            # Do FFT
            master_frequency=fft_analysis(data)#, chunk, samplerate)
           # print(master_frequency)
           

    except KeyboardInterrupt:
        print("error")
    finally:
        print ("\nStopping")
        stream.close()
        p.terminate()
        

"""def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency
    global MAX

    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    print(len(data2))
    # Apply FFT
    fourier = numpy.fft.fft(data2)

    #print(fourier)
"""
def fft_analysis(data):
    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = np.array(data2, dtype='h')
    transform=np.log10(np.abs(np.fft.rfft(data2)))
    #print("fourier_transform")
    #print(transform,len(transform))
    return int(np.argmax(transform)/2)
     
    #print("showed")
    

def amplitude_analysis(data, scale, exponent):
    rms= audioop.rms(data, 2)
    level = min(rms / (2.0 ** 16) * scale, 1.0) 
    level = level**exponent 
    level = int(level * 100
    )
    return level


    
def get_devices_info():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

def send_int_to_arduino(x):
    arduino.write(struct.pack('>B', int(x) ) )

if __name__ == '__main__':
    #list_devices()
    
    arduino_soundlight() 


    
