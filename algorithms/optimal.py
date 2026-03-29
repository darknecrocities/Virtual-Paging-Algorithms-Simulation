"""
Optimal Page Replacement Algorithm.
This algorithm replaces the page that will not be used for the longest time in the future.
When multiple pages have no future use, LRU is used as a tiebreaker (classmate's technique).
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

    # Track last used time for LRU tiebreaker when multiple pages have no future use
    last_used = {}

    for i, page in enumerate(reference_string):
        is_fault = False
        explanation = ""

        if page in frames:
            hits += 1
            last_used[page] = i
            explanation = f"Page {page} is already in memory (Hit)."
        else:
            faults += 1
            is_fault = True
            if len(frames) < num_frames:
                frames.append(page)
                last_used[page] = i
                explanation = f"Page {page} caused a fault. Added to an empty frame."
            else:
                # Look ahead into the remaining reference string
                future = reference_string[i + 1:]

                no_future = []      # Pages in frames that never appear again
                future_use = {}     # Pages in frames that do appear → next_use index

                for f_page in frames:
                    try:
                        next_use = future.index(f_page)
                        future_use[f_page] = next_use
                    except ValueError:
                        no_future.append(f_page)

                if no_future:
                    # Among pages with no future use, pick the one least recently used (LRU tiebreaker)
                    page_to_replace = min(no_future, key=lambda x: last_used.get(x, -1))
                    explanation = (
                        f"Page {page} caused a fault. Replaced page {page_to_replace} "
                        f"(never used again; chosen by LRU among never-used pages)."
                    )
                else:
                    # All pages appear in the future — replace the one used furthest away
                    page_to_replace = max(future_use, key=lambda x: future_use[x])
                    explanation = (
                        f"Page {page} caused a fault. Replaced page {page_to_replace} "
                        f"which is used furthest in the future."
                    )

                idx = frames.index(page_to_replace)
                frames[idx] = page
                last_used[page] = i

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
