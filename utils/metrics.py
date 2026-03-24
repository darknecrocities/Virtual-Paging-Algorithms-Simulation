import pandas as pd
import plotly.express as px

def plot_algorithm_comparison(results_dict):
    """
    results_dict: {
        "FIFO": {"faults": 10},
        "LRU": {"faults": 8},
        ...
    }
    """
    algorithms = list(results_dict.keys())
    faults = [res["faults"] for res in results_dict.values()]
    
    if not algorithms:
        return None
        
    df = pd.DataFrame({"Algorithm": algorithms, "Faults": faults})
    
    # Highlight the best algorithm (minimum faults)
    min_faults = min(faults)
    colors = ['#4ade80' if f == min_faults else '#a78bfa' for f in faults] # Green for best, Purple for others
    
    fig = px.bar(df, x="Algorithm", y="Faults", 
                 title="Page Faults Comparison",
                 color="Algorithm",
                 color_discrete_sequence=colors)
                 
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        showlegend=False
    )
    return fig
