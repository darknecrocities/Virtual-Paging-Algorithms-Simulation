# 🧠 Smart Page Replacement Visualizer (SPRV)

> A modern, interactive Streamlit desktop application that visualizes classic Operating System memory management and page replacement algorithms, supercharged with AI insights via Google Gemini.

## ✨ Features

- **5 Core Algorithms Implemented**: `FIFO`, `LRU`, `MRU`, `OPTIMAL`, and `Second Chance (Clock)`.
- **Stunning UI**: Custom dark mode glassmorphism theme with neon accents, moving away from default Streamlit styling.
- **Animated Playback**: Step-by-step frame visualization showing exactly how pages are mapped, hit, or faulted with playback controls.
- **AI-Powered Insights**: Integrates with the `google-genai` SDK using Gemini to analyze the memory access patterns, detect locality, and explain why certain algorithms performed better.
- **Multi-Algorithm Comparison**: Compare all 5 algorithms side-by-side with Plotly bar charts.
- **Advanced Memory Heatmaps**: Visualize spatial and temporal locality using Plotly Heatmaps.

## 📁 Project Structure

```text
Virtual-Paging-Algorithms-Simulation/
│
├── app.py                 # Main Streamlit web application
├── .env                   # Environment variables (GEMINI_API_KEY)
├── requirements.txt       # Python dependencies
│
├── algorithms/            # Core page replacement logic
│   ├── fifo.py
│   ├── lru.py
│   ├── mru.py
│   ├── optimal.py
│   └── second_chance.py
│
├── utils/                 # Helper modules
│   ├── ai_insights.py     # Connects to Gemini API for JSON insights
│   ├── analyzer.py        # Generates memory heatmaps
│   ├── generator.py       # Generates test strings (Random, Locality, Worst-case)
│   └── metrics.py         # Renders the Plotly comparison charts
│
└── assets/
    └── styles.css         # UI injection for Glassmorphism & Neon cards
```

## 🚀 How to Run

1. **Clone the repository and enter the directory**:
   ```bash
   git clone <your-repo-link>
   cd Virtual-Paging-Algorithms-Simulation
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Open the `.env` file and strictly set your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Launch the Application**:
   ```bash
   python3 -m streamlit run app.py
   ```
   The app will open automatically in your browser at `http://localhost:8501`.

## 📄 Detailed Code Documentation

This project follows a strict modular structure to maintain separation of concerns between the UI, the algorithmic logic, and the helper utilities.

### 1. Main Application (`app.py`)
This is the core entry point of the Streamlit application. It acts as the controller that binds the user interface, algorithms, and analytical tools together.
* **UI Structure**: Uses a tabbed interface (Configuration, Visualizer, AI Insights, OS Analysis) to separate workflow stages.
* **State Management**: Uses `st.session_state` extensively to manage the animation loop variables (e.g., `sim_step`, `is_playing`, `selected_algo`) preventing the app from resetting on every user interaction.
* **Rendering Loop**: Replaces legacy `st.rerun()` loops with a controlled `while` loop implementation that safely renders algorithm steps dynamically, rendering hit/miss tracking metrics in real-time glassmorphism cards.

### 2. Page Replacement Algorithms (`algorithms/`)
Each algorithm follows a strict signature: `run_algo(reference_string, num_frames)` and returns a structured dictionary containing `frames` state, `step_details` (action logs), `faults`, and `hits`.

* **`fifo.py` (First-In-First-Out)**:
  * Uses a simple queue (`list`). When a page fault occurs and physical memory is full, the oldest page (index 0) is popped, and the new page is appended.
* **`lru.py` (Least Recently Used)**:
  * Identifies the page that hasn't been used for the longest time. It continuously tracks access history, removing the page whose last usage index is the furthest in the past when a replacement is needed.
* **`mru.py` (Most Recently Used)**:
  * The conceptual opposite of LRU. When memory is full, it replaces the page that was *most recently* accessed. Commonly useful for cyclical sequential access patterns (like Database buffer pools).
* **`optimal.py` (Optimal/Belady's Algorithm)**:
  * Looks *into the future* of the reference string to predict which page will not be needed for the longest time. Acts as a theoretical upper bound benchmark for performance, as it requires perfect future knowledge.
* **`second_chance.py` (Clock Algorithm)**:
  * An approximation of LRU. Instead of heavy timestamps, it maintains a circular queue (`pointer`) and a parallel array of `reference_bits`.
  * If a page is accessed, its bit is set to `1`.
  * If a replacement is needed, the pointer sweeps the frames. If it finds a `1`, it gives it a "second chance", sets it to `0`, and moves on. If it finds a `0`, that page is replaced.

### 3. Utility Modules (`utils/`)
* **`ai_insights.py`**:
  * Initializes the `google-genai` client using the `GEMINI_API_KEY` from the `.env` file. 
  * Constructs an analytical prompt embedding the simulated faults/hits, and explicitly requests the Gemini 3.1 Flash (Preview) model to return its evaluation strictly as a JSON payload, avoiding markdown formatting issues.
* **`generator.py`**:
  * **`generate_random()`**: Produces a completely unpatterned string of page accesses.
  * **`generate_locality()`**: Simulates realistic clustered memory accesses (e.g., loops and arrays) where the CPU repeatedly accesses a tight subset of pages.
  * **`generate_worst_case()`**: Intentionally generates adversarial sequences (like `1, 2, 3, 4, 1, 2...`) designed to trigger devastating page fault storms (Belady's Anomaly) on algorithms like FIFO.
* **`analyzer.py`**:
  * Contains `detect_locality()` which iterates over the reference string to calculate duplicate sequential or near-sequential access frequencies to definitively classify whether an inputted pattern exhibits high spacial/temporal locality.
* **`metrics.py`**:
  * Uses `Plotly Express` to generate professional, interactive bar charts plotting Hits vs Faults for all selected algorithms, automatically dynamically scaling based on application width parameters.

### 4. Aesthetics (`assets/`)
* **`styles.css`**:
  * Injects pure CSS bypassing Streamlit's default components. Forces `st.container` elements to inherit `glass-card` styling (blurry translucent backgrounds with neon cyan/purple SVG borders).
