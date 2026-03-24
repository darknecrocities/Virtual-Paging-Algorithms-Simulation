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

## 🤖 Code Documentation Overview

* **`app.py`**: The entry point. Handles all routing, UI tabs, state management (session state for animations), and parsing of JSON payloads from the AI.
* **`algorithms/*.py`**: Each file returns a standardized dictionary payload containing:
  - `frames`: An array representing the physical memory state at each sequence step.
  - `step_details`: Explanatory logs for exactly *why* a fault or hit occurred.
  - `faults` / `hits`: Statistical performance numbers.
* **`utils/ai_insights.py`**: Connects to the newest Gemini models using the `google-genai` client, forcing the API to return strictly structured JSON representing analytical insights, which the frontend renders as beautiful glass UI cards.
