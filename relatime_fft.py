import pyaudio
import numpy as np
import time
import wave
import matplotlib.pyplot as plt


# open stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

CHUNK = 2048 # RATE / number of updates per second

RECORD_SECONDS = 20


# use a Blackman window
window = np.blackman(CHUNK)

x = 0

def soundPlot(stream):
    t1=time.time()
    data = stream.read(CHUNK, exception_on_overflow=False)
    waveData = wave.struct.unpack("%dh"%(CHUNK), data)
    npArrayData = np.array(waveData)
    indata = npArrayData*window
    #Plot time domain
   
    fftData=np.abs(np.fft.rfft(indata))
    fftTime=np.fft.rfftfreq(CHUNK, 1./RATE)
    which = fftData[1:].argmax() + 1
    #Plot frequency domain graph
    print(fftTime)
    print(len(fftData))
    print("took %.02f ms"%((time.time()-t1)*1000))
    # use quadratic interpolation around the max
    # if which != len(fftData)-1:
    #     y0,y1,y2 = np.log(fftData[which-1:which+2:])
    #     x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
    #     # find the frequency and output it
    #     thefreq = (which+x1)*RATE/CHUNK
    #     print ("The freq is %f Hz." % (thefreq) )
    # else:
    #     thefreq = which*RATE/CHUNK
    #     print ("The freq is %f Hz." % (thefreq) )

if __name__=="__main__":
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)


    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS) ):
        soundPlot(stream)

    stream.stop_stream()
    stream.close()
    p.terminate()