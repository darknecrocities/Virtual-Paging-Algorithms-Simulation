"""
Optimal Page Replacement Algorithm.
This algorithm replaces the page that will not be used for the longest time in the future.
Used purely as a theoretical benchmark.
"""

def run_optimal(reference_string, num_frames):
    """
    Simulates the Optimal page replacement algorithm.
    :param reference_string: List of integers representing memory page requests.
    :param num_frames: Integer representing available physical memory frames.
    :return: Dictionary containing step-by-step states, faults, and hit statistics.
    """
    frames = []
    faults = 0
    hits = 0
    step_details = []
    frame_states = []
    
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
                explanation = f"Page {page} caused a fault. Added to an empty frame."
            else:
                # Look ahead to find the page to replace
                farthest_use = -1
                page_to_replace = None
                
                for f_page in frames:
                    try:
                        # Find next occurrence of f_page in the remaining string
                        next_use = reference_string[i+1:].index(f_page)
                    except ValueError:
                        # f_page is not used again, it's the perfect candidate
                        page_to_replace = f_page
                        break
                    
                    if next_use > farthest_use:
                        farthest_use = next_use
                        page_to_replace = f_page
                
                if not page_to_replace:
                    page_to_replace = frames[0] # Fallback
                
                idx = frames.index(page_to_replace)
                frames[idx] = page
                explanation = f"Page {page} caused a fault. Replaced page {page_to_replace} which is used furthest in the future."
                
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
