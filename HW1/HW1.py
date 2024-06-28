# AmirHossein Tajiki 99312207
# Requirements: librosa, sounddevice, numpy, ffmpeg PATH


import librosa
import sounddevice as sd
import numpy



y_laptop, sr_laptop  = librosa.load('laptop-48k.m4a', sr=None)          # Sr=None to Avoid Sr convertion to 22k, by default load() will convert sr to 22k
y_earbuds, sr_earbuds  = librosa.load('earbuds-16k.m4a', sr=None)

print("-"*75)
# NOTE: I guess warnings are because the PySoundFile module dosent support m4a and librosa.load() uses audioread as fallback and its deprecated.

y_laptop_pre_emphasized = librosa.effects.preemphasis(y_laptop, coef=0.92)
y_earbuds_pre_emphasized = librosa.effects.preemphasis(y_earbuds, coef=0.92)

time_laptop = len(y_laptop_pre_emphasized) / sr_laptop
time_earbuds = len(y_earbuds) / sr_earbuds


# 20ms frames with hop of 5ms
frame_interval_millisecond = 20
overlap_interval_millisecond = 5

# Laptop 
frame_intervals_laptop_count = int((frame_interval_millisecond / 1000) * sr_laptop)           # convertion of millisecond to samples
overlap_intervals_laptop_count = int((overlap_interval_millisecond / 1000) * sr_laptop)
frames_laptop = librosa.util.frame(y_laptop_pre_emphasized, frame_length=frame_intervals_laptop_count, hop_length=overlap_intervals_laptop_count)


# Earbuds
frame_intervals_earbuds_count = int((frame_interval_millisecond / 1000) * sr_earbuds)           # convertion of millisecond to samples
overlap_intervals_earbuds_count = int((overlap_interval_millisecond / 1000) * sr_earbuds)
frames_earbuds = librosa.util.frame(y_earbuds_pre_emphasized, frame_length=frame_intervals_earbuds_count, hop_length=overlap_intervals_earbuds_count)


# NOTE: util.frame(): axis=0 framing on first dimension, axis=-1 framing on last dimension.       default = 0
# NOTE: numpy.ndarray.mean(): axis=0 do sum on the rows , axis=1 does summation on columns.
# e.g:  [[1, 2, 3], [4, 5, 6]];        axis=0: [2.5, 3.5, 4.5]       axis=1: [2, 5]



 
# Get avg of framing sets
avg_frames_laptop = frames_laptop.mean(axis=1)
avg_frames_earbuds = frames_earbuds.mean(axis=1)

# Return framing set with max value 
maximum_laptop =  avg_frames_laptop.max()
maximum_earbuds = avg_frames_earbuds.max()

index_laptop  = numpy.where(avg_frames_laptop == maximum_laptop)
index_earbuds  = numpy.where(avg_frames_earbuds == maximum_earbuds)


print(f"Length of Voice LAPTOP: {time_laptop:.3f}s, number of samples: {len(y_laptop_pre_emphasized)}, sr: {sr_laptop}")
print(f"Frames Count: {frame_intervals_laptop_count} (20ms), Hop Count: {overlap_intervals_laptop_count} (5ms)")
print(f"Maximum Framing Set Index: {index_laptop[0]}")
sd.play(y_laptop_pre_emphasized, sr_laptop)
sd.wait()

print("_" * 50)

print(f"Length of Voice EARBUDS: {time_earbuds:.3f}s, number of samples: {len(y_earbuds_pre_emphasized)}, sr: {sr_earbuds}")
print(f"Franes Count: {frame_intervals_earbuds_count} (20ms), Hop Count: {overlap_intervals_earbuds_count} (5ms)")
print(f"Maximum Framing Set Index: {index_earbuds[0]}")
sd.play(y_earbuds_pre_emphasized, sr_earbuds)
sd.wait()

