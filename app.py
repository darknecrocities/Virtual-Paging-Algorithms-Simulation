"""
Smart Page Replacement Visualizer (SPRV)
Main Streamlit Application. Handles UI, interactions, charting, and AI API calls.
"""

import streamlit as st
import pandas as pd
import time
import os
import json

from algorithms.fifo import run_fifo
from algorithms.lru import run_lru
from algorithms.mru import run_mru
from algorithms.optimal import run_optimal
from algorithms.second_chance import run_second_chance
from utils.generator import generate_random_string, generate_locality_string, generate_worst_case_string
from utils.metrics import plot_algorithm_comparison
from utils.analyzer import detect_locality, plot_memory_heatmap
from utils.ai_insights import generate_ai_insights

st.set_page_config(page_title="SPRV | Smart Page Replacement Visualizer", layout="wide", page_icon="🧠")

def inject_css():
    try:
        with open("assets/styles.css", "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        pass

def get_algorithm_map():
    return {
        "FIFO": run_fifo,
        "LRU": run_lru,
        "MRU": run_mru,
        "OPTIMAL": run_optimal,
        "Second Chance (Clock)": run_second_chance
    }

def process_reference_string(input_str):
    try:
        return [int(x.strip()) for x in input_str.split(",") if x.strip()]
    except ValueError:
        st.error("Invalid reference string format. Please use comma-separated integers.")
        return []

def main():
    inject_css()
    
    st.markdown("<h1 class='neon-cyan'>🧠 Smart Page Replacement Visualizer (SPRV)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Interactive OS memory simulation with AI-driven insights.</p>", unsafe_allow_html=True)
               
    # Initialize session state variables
    if "ref_string" not in st.session_state:
        st.session_state.ref_string = "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1"
        
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h3 class='neon-purple'>⚙️ Configuration</h3>", unsafe_allow_html=True)
        
        # Test Case Generators
        st.markdown("<b>Data Generators</b>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        if col1.button("🎲 Random", help="Generate Random Input"):
            st.session_state.ref_string = ", ".join(map(str, generate_random_string(20)))
            st.rerun()
        if col2.button("📊 Locality", help="Generate Locality-Based Input"):
            st.session_state.ref_string = ", ".join(map(str, generate_locality_string(20)))
            st.rerun()
        if col3.button("💥 Worst", help="Generate Worst-case scenario for LRU/FIFO"):
            st.session_state.ref_string = ", ".join(map(str, generate_worst_case_string(4, 20)))
            st.rerun()
            
        uploaded_file = st.file_uploader("📂 Upload .txt file (comma separated)", type=["txt", "csv"])
        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8")
            st.session_state.ref_string = content.strip()
            
        ref_input_str = st.text_area("Reference String (comma-separated)", value=st.session_state.ref_string, height=100)
        
        num_frames = st.number_input("Number of Frames", min_value=1, max_value=10, value=3)
        
        algos = list(get_algorithm_map().keys())
        selected_algos = st.multiselect("Select Algorithms", algos, default=["FIFO", "LRU"])
        
        st.markdown("<hr>", unsafe_allow_html=True)
        run_btn = st.button("▶ Run Simulation", width='stretch')
        
    # Validation
    ref_string_arr = process_reference_string(ref_input_str)
        
    tabs = st.tabs(["👁️ Visualization", "📊 Comparison Mode", "💡 AI Insights", "📚 OS Analysis"])
    
    # Store results in session state to avoid re-calculating unless required
    if run_btn and ref_string_arr and selected_algos:
        results = {}
        algo_map = get_algorithm_map()
        for algo in selected_algos:
            results[algo] = algo_map[algo](ref_string_arr, num_frames)
        st.session_state.sim_results = results
        st.session_state.sim_ref_string = ref_string_arr
        st.session_state.sim_frames = num_frames
        
    if "sim_results" in st.session_state:
        results = st.session_state.sim_results
        ref_arr = st.session_state.sim_ref_string
        
        # --- TAB 1: VISUALIZATION ---
        with tabs[0]:
            st.markdown("<h3 class='neon-cyan'>Step-by-Step Visualization</h3>", unsafe_allow_html=True)
            
            # Select specific algorithm to visualize if multiple chosen
            vis_algo = st.selectbox("Select Algorithm to Visualize", list(results.keys()))
            data = results[vis_algo]
            
            # Sub-tabs for Animation vs Details
            vis_tabs = st.tabs(["🎬 Animation", "📋 Step Table"])
            
            with vis_tabs[0]:
                st.markdown("<hr>", unsafe_allow_html=True)
                
                if "anim_step" not in st.session_state:
                    st.session_state.anim_step = 0
                if "is_playing" not in st.session_state:
                    st.session_state.is_playing = False
                    
                # Center-aligned symmetrical animation controls
                _, animcol1, animcol2, animcol3, animcol4, _ = st.columns([2, 1, 1, 1, 1, 2])
                
                if animcol1.button("▶ Play"):
                    st.session_state.is_playing = True
                    st.rerun()
                if animcol2.button("⏸ Pause"):
                    st.session_state.is_playing = False
                    st.rerun()
                if animcol3.button("⏭ Next"):
                    if st.session_state.anim_step < len(ref_arr):
                        st.session_state.anim_step += 1
                    st.session_state.is_playing = False
                    st.rerun()
                if animcol4.button("🔄 Reset"):
                    st.session_state.anim_step = 0
                    st.session_state.is_playing = False
                    st.rerun()
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Symmetrical containers
                metrics_container = st.empty()
                st.markdown("<br>", unsafe_allow_html=True)
                
                colA, colB, colC = st.columns([1, 2, 1])
                with colB:
                    frame_container = st.empty()
                    status_container = st.empty()

                def render_frame(step_idx):
                    if step_idx == 0:
                        with metrics_container.container():
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Page Faults", 0)
                            m2.metric("Page Hits", 0)
                            m3.metric("Fault Rate", "0.0%")
                            m4.metric("Success Rate", "0.0%")
                        frame_container.markdown(f"<h3 style='text-align: center;'>Ready to start</h3>", unsafe_allow_html=True)
                        status_container.info("Click Play or Next to begin simulation.")
                        return

                    real_idx = step_idx - 1
                    step_data = data['step_details'][real_idx]
                    
                    cur_hits = sum(1 for i in range(step_idx) if data['step_details'][i]['Status'] == 'Hit')
                    cur_faults = sum(1 for i in range(step_idx) if data['step_details'][i]['Status'] == 'Fault')
                    
                    with metrics_container.container():
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Page Faults", cur_faults)
                        m2.metric("Page Hits", cur_hits)
                        m3.metric("Fault Rate", f"{(cur_faults/max(1, step_idx))*100:.1f}%")
                        m4.metric("Success Rate", f"{(cur_hits/max(1, step_idx))*100:.1f}%")

                    html_frames = "<div style='display: flex; justify-content: center;'>"
                    for f in data['frames'][real_idx]:
                        status_class = "empty" if f == "-" else ("hit" if step_data['Status'] == 'Hit' else "fault")
                        html_frames += f"<div class='frame-box {status_class}'>{f}</div>"
                    html_frames += "</div>"
                        
                    frame_container.markdown(f"<div style='text-align: center;'><b>Step {step_idx} | Page Request: <span class='neon-cyan' style='font-size: 1.5rem;'>{step_data['Page']}</span></b><br><br>{html_frames}</div>", unsafe_allow_html=True)
                    status_container.info(step_data['Explanation'])

                # Render initial state
                render_frame(st.session_state.anim_step)
                
                # If playing, run the loop inline for smooth updates
                if st.session_state.is_playing:
                    while st.session_state.anim_step < len(ref_arr):
                        time.sleep(1) # animation delay
                        st.session_state.anim_step += 1
                        render_frame(st.session_state.anim_step)
                    
                    st.session_state.is_playing = False
                    st.rerun() # Refresh button states at end
                        
            with vis_tabs[1]:
                st.markdown("### Execution Log")
                df = pd.DataFrame(data['step_details'])
                st.dataframe(df, width='stretch')
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Action Log (.csv)", csv, f"{vis_algo}_log.csv", "text/csv")
                
                
        # --- TAB 2: COMPARISON MODE ---
        with tabs[1]:
            st.markdown("<h3 class='neon-purple'>Multi-Algorithm Comparison</h3>", unsafe_allow_html=True)
            if len(results) > 1:
                # Top metrics side-by-side
                cols = st.columns(len(results))
                for i, (algo, res) in enumerate(results.items()):
                    with cols[i]:
                        st.markdown(f"<div class='glass-card'><h4>{algo}</h4><p class='neon-cyan'>Faults: {res['faults']}</p><p>Hits: {res['hits']}</p><p>Hit Rate: {res['success_rate']*100:.1f}%</p></div>", unsafe_allow_html=True)
                
                st.plotly_chart(plot_algorithm_comparison(results), width='stretch')
            else:
                st.warning("Select at least 2 algorithms in the sidebar to compare.")
                
            st.markdown("### Memory Heatmap & Locality")
            local_status = detect_locality(ref_arr)
            st.info(f"**Locality Detector:** {local_status}")
            st.plotly_chart(plot_memory_heatmap(ref_arr), width='stretch')

        # --- TAB 3: AI INSIGHTS ---
        with tabs[2]:
            st.markdown("### Google Gemini AI Analysis")
            if st.button("🤖 Generate AI Insights"):
                with st.spinner("Analyzing memory patterns via Gemini..."):
                    # Format results for AI
                    compact_results = ""
                    for algo, r in results.items():
                        compact_results += f"{algo}: {r['faults']} faults, {r['hits']} hits, {r['success_rate']*100:.1f}% Hit Rate\n"
                    
                    ai_reply = generate_ai_insights(str(ref_arr), compact_results)
                    st.success("Analysis Complete!")
                    
                    try:
                        import json
                        data = json.loads(ai_reply)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"<div class='glass-card'><h4 class='neon-cyan'>🏆 Best Algorithm</h4><p><b>{data.get('best_algorithm', 'N/A')}</b><br>{data.get('best_why', '')}</p></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='glass-card'><h4 class='neon-cyan'>🔍 Locality Detection</h4><p>{data.get('locality', '')}</p></div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"<div class='glass-card'><h4 class='neon-purple'>📈 Performance</h4><p>{data.get('performance_explanation', '')}</p></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='glass-card'><h4 class='neon-purple'>💻 OS Relevance</h4><p>{data.get('os_relevance', '')}</p></div>", unsafe_allow_html=True)
                    except Exception:
                        # Fallback if Gemini didn't return perfect JSON
                        st.markdown(f"<div class='glass-card'>{ai_reply}</div>", unsafe_allow_html=True)

        # --- TAB 4: OS ANALYSIS ---
        with tabs[3]:
            st.markdown("### Operating System Relevance")
            st.markdown("""
            **FIFO (First-In-First-Out)**
            - *OS Relevance:* Low. Modern OSes rarely use pure FIFO due to Belady's Anomaly.
            - *Usage:* Batch scheduling or simple buffering.
            
            **LRU (Least Recently Used)**
            - *OS Relevance:* High. Forms the basis of modern memory management (e.g. Linux approximations).
            - *Usage:* Linux heavily relies on LRU variants for page cache. Windows uses a working-set model that behaves similarly.
            
            **MRU (Most Recently Used)**
            - *OS Relevance:* Niche. 
            - *Usage:* Databases often use MRU for managing buffer caches when large sequential scans occur, preferring to throw away just-read data as it won't be needed again soon.
            
            **OPTIMAL**
            - *OS Relevance:* None (Theoretical only).
            - *Usage:* Used purely as a benchmark to grade other algorithms since looking into the future is impossible in real systems.
            
            **Second Chance / Clock Algorithm**
            - *OS Relevance:* Extremely High.
            - *Usage:* Hardware lacks the ability to track exact LRU timestamps efficiently. The Clock algorithm uses a 'reference bit' tracked by the CPU. This is exactly what Linux, Windows, and macOS do under the hood to approximate LRU efficiently.
            """)
            
            
if __name__ == "__main__":
    main()
