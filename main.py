import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import argparse 
import os       

# 1. Setup CLI
parser = argparse.ArgumentParser(description="Precision Metronome & Beat Analysis Engine")
parser.add_argument("filepath", type=str, help="Path to the audio file")
args = parser.parse_args()

if not os.path.exists(args.filepath):
    print(f"Error: Could not find '{args.filepath}'")
    exit()

# 2. Load Audio
print(f"Analyzing {args.filepath}...")
y, sr = librosa.load(args.filepath)

# 3. Precision Beat Tracking
# tightness=100 helps keep the tempo estimation steady
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=100)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

# 4. Generate the "Ideal" Mathematical Metronome
# We start the metronome at the first detected beat
start_time = beat_times[0]
beat_duration = 60.0 / bpm # Seconds per beat
total_duration = librosa.get_duration(y=y, sr=sr)

# Create a list of perfect timestamps based purely on the BPM
ideal_metronome = np.arange(start_time, total_duration, beat_duration)

# 5. Visualizing the Comparison
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 6))

# Plot Waveform
librosa.display.waveshow(y, sr=sr, color='#444444', alpha=0.6, label='Audio Waveform')

# Plot the "Ideal" Metronome (The Mathematical Truth)
# We'll use Blue Dashed lines for the 'Perfect' computer timing
for i, t in enumerate(ideal_metronome):
    lbl = 'Ideal Metronome (BPM)' if i == 0 else ""
    ax.axvline(x=t, color='#00CCFF', linestyle='--', linewidth=1.5, alpha=0.5, label=lbl)

# Plot the "Detected" Beats (The Real Audio Hits)
# We'll use Bright Red lines for where the drummer actually hit
for i, t in enumerate(beat_times):
    lbl = 'Detected Audio Beats' if i == 0 else ""
    ax.axvline(x=t, color='#FF3366', linestyle='-', linewidth=2, alpha=0.9, label=lbl)

# Final Formatting
ax.set_title(f'BPM Accuracy Analysis: {bpm:.2f} BPM', fontsize=16, fontweight='bold')
ax.set_xlabel('Time (Seconds)')
ax.set_ylabel('Amplitude')
ax.legend(loc='upper right', facecolor='black')
plt.tight_layout()

print(f"\nAnalysis Complete!")
print(f"Calculated BPM: {bpm:.2f}")
print(f"Blue Dashed = Perfect Clock | Red Solid = Actual Audio")
# Calculate the drift at the end of the file
final_ideal = ideal_metronome[-1]
final_actual = beat_times[-1]
total_drift = final_actual - final_ideal

print(f"--- Drift Analysis ---")
print(f"Total Phase Drift: {total_drift:.4f} seconds")
if abs(total_drift) > 0.1:
    print("Status: Significant Drift Detected (Likely human performance or BPM rounding)")
else:
    print("Status: Clock Synced (High precision timing)")
plt.show()