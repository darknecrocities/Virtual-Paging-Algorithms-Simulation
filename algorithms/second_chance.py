"""
Second Chance (Clock) Page Replacement Algorithm.
An approximation of LRU. Checks a reference bit before replacing. 
If 1, gives a second chance and flips to 0. If 0, replaces it.
"""

def run_second_chance(reference_string, num_frames):
    """
    Simulates the Second Chance page replacement algorithm.
    :param reference_string: List of integers representing memory page requests.
    :param num_frames: Integer representing available physical memory frames.
    :return: Dictionary containing step-by-step states, faults, and hit statistics.
    """
    frames = []
    reference_bits = []
    pointer = 0
    faults = 0
    hits = 0
    step_details = []
    frame_states = []
    
    for i, page in enumerate(reference_string):
        is_fault = False
        explanation = ""
        
        if page in frames:
            hits += 1
            idx = frames.index(page)
            reference_bits[idx] = 1 # Give second chance
            explanation = f"Page {page} is already in memory (Hit). Set its reference bit to 1."
        else:
            faults += 1
            is_fault = True
            if len(frames) < num_frames:
                frames.append(page)
                reference_bits.append(0) # Initially 0 when loaded
                explanation = f"Page {page} caused a fault. Added to an empty frame."
            else:
                # Replace logic
                while True:
                    if reference_bits[pointer] == 0:
                        # Replace
                        old_page = frames[pointer]
                        frames[pointer] = page
                        reference_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames
                        explanation = f"Page {page} caused a fault. Replaced {old_page} (reference bit was 0)."
                        break
                    else:
                        # Give second chance
                        reference_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames
                
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
