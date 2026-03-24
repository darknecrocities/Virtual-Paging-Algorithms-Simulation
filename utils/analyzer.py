from collections import Counter
import plotly.express as px

def detect_locality(reference_string):
    if not reference_string:
        return "No Data"
        
    repeats = 0
    for i in range(1, len(reference_string)):
        if reference_string[i] == reference_string[i-1]:
            repeats += 1
            
    counts = Counter(reference_string)
    most_common_freq = counts.most_common(1)[0][1] if counts else 0
    avg_freq = len(reference_string) / len(counts) if counts else 0
    
    if repeats >= len(reference_string) * 0.2:
        return "High Spatial/Temporal Locality Detected (Many consecutive repeats)"
    elif most_common_freq >= avg_freq * 2 and len(counts) > 1:
        return "High Temporal Locality Detected (Few pages heavily accessed)"
    else:
        return "Low Locality Detected (Random access pattern)"

def plot_memory_heatmap(reference_string):
    if not reference_string:
        return None
        
    max_page = max(reference_string)
    data = []
    
    for page in range(max_page + 1):
        row = [1 if ref == page else 0 for ref in reference_string]
        decayed_row = []
        val = 0
        for x in row:
            if x == 1:
                val = 1.0
            else:
                val = max(0, val - 0.2)
            decayed_row.append(val)
        data.append(decayed_row)
        
    fig = px.imshow(data, 
                    labels=dict(x="Sequence Step", y="Page Number", color="Activity"),
                    x=list(range(1, len(reference_string) + 1)),
                    y=list(range(max_page + 1)),
                    color_continuous_scale="Purp" # Purple accent
                   )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        title="Memory Access Heatmap (Activity Trace)",
        yaxis=dict(tick0=0, dtick=1)
    )
    return fig
