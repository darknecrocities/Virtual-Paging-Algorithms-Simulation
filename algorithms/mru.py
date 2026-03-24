"""
Most Recently Used (MRU) Page Replacement Algorithm.
This algorithm replaces the page that was very recently used. Common in DB buffer pools.
"""

def run_mru(reference_string, num_frames):
    """
    Simulates the MRU page replacement algorithm.
    :param reference_string: List of integers representing memory page requests.
    :param num_frames: Integer representing available physical memory frames.
    :return: Dictionary containing step-by-step states, faults, and hit statistics.
    """
    frames = []
    faults = 0
    hits = 0
    step_details = []
    frame_states = []
    
    last_used = {}
    
    for i, page in enumerate(reference_string):
        is_fault = False
        explanation = ""
        
        if page in frames:
            hits += 1
            last_used[page] = i
            explanation = f"Page {page} is already in memory (Hit). Updated its last used time."
        else:
            faults += 1
            is_fault = True
            if len(frames) < num_frames:
                frames.append(page)
                last_used[page] = i
                explanation = f"Page {page} caused a fault. Added to an empty frame."
            else:
                # Find the most recently used page in frames
                mru_page = max(frames, key=lambda x: last_used.get(x, -1))
                idx = frames.index(mru_page)
                frames[idx] = page
                last_used[page] = i
                explanation = f"Page {page} caused a fault. Replaced the most recently used page {mru_page}."
                
        frame_copy = frames.copy()
        while len(frame_copy) < num_frames:
            frame_copy.append("-")
            
        frame_states.append(frame_copy)
        
        step_details.append({
            "Step": i + 1,
            "Page": page,
            "Frame State": str(frame_copy).replace("'", ""),
            "Status": "Fault" if is_fault else "Hit",
            "Explanation": explanation
        })
        
    total_references = len(reference_string)
    fault_rate = faults / total_references if total_references > 0 else 0
    success_rate = hits / total_references if total_references > 0 else 0
    
    return {
        "frames": frame_states,
        "faults": faults,
        "hits": hits,
        "fault_rate": fault_rate,
        "success_rate": success_rate,
        "step_details": step_details
    }
