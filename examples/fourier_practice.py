import numpy as np
from matplotlib import pyplot as plt

# frequency is the number of times a wave repeats a second
frequency = 1000
noisy_freq = 50
num_samples = 48000
 
# The sampling rate of the analog to digital convert
sampling_rate = 48000.0

#Create the sine wave and noise
sine_wave = [np.sin(2 * np.pi * frequency * x1 / sampling_rate) for x1 in range(num_samples)]
sine_noise = [np.sin(2 * np.pi * noisy_freq * x1/  sampling_rate) for x1 in range(num_samples)]
 
#Convert them to numpy arrays
sine_wave = np.array(sine_wave)
sine_noise = np.array(sine_noise)

# Add them to create a noisy signal
combined_signal = sine_wave + sine_noise
plt.subplot(4,1,1)
plt.title("Original sine wave")
# Need to add empty space, else everything looks scrunched up!
plt.subplots_adjust(hspace=2)
plt.plot(sine_wave[:500])

plt.subplot(4,1,2)
plt.title("Noisy wave")
plt.plot(sine_noise[:4000])

plt.subplot(4,1,3)
plt.title("Original + Noise")
plt.plot(combined_signal[:3000])


data_fft = np.fft.fft(combined_signal)
freq = (np.abs(data_fft[:len(data_fft)]))

plt.subplot(4,1,4)
plt.plot(freq)
plt.title("Before filtering: Will have main signal (1000Hz) + noise frequency (50Hz)")
plt.xlim(20,20_000)
plt.xscale('log')


plt.show()