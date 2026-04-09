# 🥁 Precision Rhythm & Metronome Analysis Engine

A desktop-based Digital Signal Processing (DSP) tool developed to quantify rhythmic precision in audio signals. This system analyzes raw audio transients and compares them against a mathematically synthesized periodic reference to calculate BPM, timing jitter, and accumulated clock drift.

Developed as a personal project to bridge Software Engineering, Signal Processing, and UX Design.

## 🚀 Key Features
* **Automated Beat Tracking:** Leverages spectral flux onset strength and dynamic programming to identify rhythmic pulses in complex audio.
* **Ideal Metronome Synthesis:** Generates a perfect periodic reference grid using the formula $t_n = t_{start} + (n \times T)$ where $T$ is the beat period.
* **Drift Quantification:** Quantifies the phase error (drift) between real-world performance and mathematical perfection, useful for analyzing "human feel" vs. robotic timing.
* **Interactive GUI:** A local web-based dashboard built with Streamlit for seamless drag-and-drop audio analysis and visualization.

## 📊 Expected Output & Visualization
Upon uploading a `.wav` or `.mp3` file, the engine provides:
* **Real-time Metrics:** High-level display of calculated BPM, total beat count, and final clock drift.
* **Dual-Layer Waveform Plot:**
    * **Solid Red Lines:** Exact detected audio transients (the "Real" timing).
    * **Dashed Blue Lines:** The ideal mathematical metronome (the "Truth").
* **Jitter Analysis:** (Terminal output) Standard deviation of beat intervals to assess rhythmic consistency.

## 🛠️ Requirements & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YourUsername/RhythmAnalysisEngine.git](https://github.com/YourUsername/RhythmAnalysisEngine.git)
   cd RhythmAnalysisEngine
