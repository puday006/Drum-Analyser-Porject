import streamlit as st
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Rhythm Analysis Engine", layout="wide")
st.title("🥁 Precision Rhythm & Metronome Analysis")
st.write("Zoom in to the millisecond level to inspect rhythmic jitter and phase drift.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("1. Analysis Settings")
bpm_hint = st.sidebar.number_input("BPM Hint (Optional)", min_value=0, max_value=250, value=0, 
                                 help="Helps the AI avoid 'Double-Time' errors.")
tightness = st.sidebar.slider("Metronome Tightness", 0, 500, 100, 
                             help="Higher = more rigid grid; Lower = follows the drummer.")

st.sidebar.header("2. 🔍 Viewport (Oscilloscope Mode)")
# Micro-zoom allowed down to 0.1 seconds
zoom_window = st.sidebar.slider("Zoom Window (Seconds)", min_value=0.1, max_value=30.0, value=2.0)
start_sec = st.sidebar.number_input("Start Position (Seconds)", min_value=0.0, step=0.5, value=0.0)

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload Audio (WAV or MP3)", type=['wav', 'mp3'])

if uploaded_file is not None:
    # Save temp file
    temp_filename = "temp_audio_file.wav"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        with st.spinner('Analyzing Signal...'):
            # 1. Load Signal
            y, sr = librosa.load(temp_filename)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # 2. Beat Tracking
            if bpm_hint > 0:
                tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=tightness, start_bpm=bpm_hint)
            else:
                tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, tightness=tightness)
                
            beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
            
            # 3. Ideal Metronome Synthesis
            start_time = beat_times[0]
            beat_duration = 60.0 / bpm
            ideal_metronome = np.arange(start_time, duration, beat_duration)
            
            # 4. Drift Calculation
            final_drift = beat_times[-1] - ideal_metronome[-1]

        # --- METRICS DASHBOARD ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Detected BPM", f"{bpm:.2f}")
        c2.metric("Total Beats", len(beat_times))
        c3.metric("Final Phase Drift", f"{final_drift:.4f}s", delta=f"{final_drift:.4f}s", delta_color="inverse")

        # --- VISUALIZATION ---
        st.subheader(f"Detailed View: {start_sec}s to {start_sec + zoom_window}s")
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(14, 5))
        
        # Plot Audio Waveform
        librosa.display.waveshow(y, sr=sr, color='#444444', alpha=0.5, ax=ax, label='Waveform')
        
        # Plot Ideal Grid (Blue Dashed) - Only in view range for performance
        for t in ideal_metronome:
            if start_sec <= t <= (start_sec + zoom_window):
                ax.axvline(x=t, color='#00CCFF', linestyle='--', linewidth=1.5, alpha=0.6)
            
        # Plot Actual Beats (Red Solid) - Only in view range
        for t in beat_times:
            if start_sec <= t <= (start_sec + zoom_window):
                ax.axvline(x=t, color='#FF3366', linestyle='-', linewidth=2.5, alpha=0.9)

        # Apply the Zoom
        ax.set_xlim(start_sec, start_sec + zoom_window)
        ax.set_ylim(-1, 1) # Normalizes amplitude height
        ax.set_xlabel("Time (Seconds)")
        ax.set_ylabel("Amplitude")
        
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error processing audio: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

else:
    st.info("Please upload an audio file to begin analysis.")

    # --- INFORMATION EXPANDER ---
with st.expander("ℹ️ How to read this analysis"):
            st.markdown("""
            ### The Comparison Logic
            This engine compares your audio against a **Mathematical Truth**.
            
            * **🔴 Red Solid Lines (Detected Beats):** These represent the *actual* transients detected in your audio file. They show exactly when the drummer hit the drum.
            * **🔵 Blue Dashed Lines (Ideal Metronome):** This is a perfectly periodic grid synthesized at the detected BPM. It represents a 'Perfect Robot' timing.
            
            ### What is Phase Drift?
            **Phase Drift** is the accumulated timing error over the duration of the track. 
            * If the **Red line** is to the **right** of the Blue line, the performer is playing **behind the beat** (Late).
            * If the **Red line** is to the **left**, the performer is **rushing** (Early).
            
            A 'Phase Drift' of `0.050s` means that by the end of the song, the performer is 50 milliseconds out of sync with a perfect clock.
            """)

        # --- METRICS DASHBOARD ---
c1, c2, c3 = st.columns(3)
        # ... (rest of your metrics code)