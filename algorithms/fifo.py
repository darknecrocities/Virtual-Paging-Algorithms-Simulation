"""
First-In-First-Out (FIFO) Page Replacement Algorithm.
This algorithm replaces the oldest page in memory.
"""

def run_fifo(reference_string, num_frames):
    """
    Simulates the FIFO page replacement algorithm.
    :param reference_string: List of integers representing memory page requests.
    :param num_frames: Integer representing available physical memory frames.
    :return: Dictionary containing step-by-step states, faults, and hit statistics.
    """
    frames = []
    faults = 0
    hits = 0
    step_details = []
    frame_states = []
    
    # FIFO queue to keep track of the order of pages added
    queue = []
    
    for i, page in enumerate(reference_string):
        is_fault = False
        explanation = ""
        
        if page in frames:
            hits += 1
            explanation = f"Page {page} is already in memory (Hit)."
        else:
            faults += 1
            is_fault = True
            if len(frames) < num_frames:
                frames.append(page)
                queue.append(page)
                explanation = f"Page {page} caused a fault. Added to an empty frame."
            else:
                # Remove the oldest page
                oldest_page = queue.pop(0)
                # Replace in frames list
                idx = frames.index(oldest_page)
                frames[idx] = page
                queue.append(page)
                explanation = f"Page {page} caused a fault. Replaced the oldest page {oldest_page}."
        
        frame_copy = frames.copy()
        # pad with '-' if not full
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
