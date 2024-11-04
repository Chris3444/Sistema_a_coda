# EXTERNAL LIBRARIES #
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import unicodeit

# CUSTOM LIBRARIES #
from static import STATIC_RESULTS
from simulation import SIMULATION_RESULTS


# STATIC PLOTS INITIALIZATION #
packet_queue_subplot = make_subplots(rows=1, cols=2, subplot_titles=("Simulation", "Static"), shared_yaxes=True)
packet_subplot = make_subplots(rows=1, cols=2, subplot_titles=("Simulation", "Static"), shared_yaxes=True)
time_subplot = make_subplots(rows=1, cols=2, subplot_titles=("Simulation", "Static"), shared_yaxes=True)

for i in STATIC_RESULTS['packet_queue_plot'].data:
    packet_queue_subplot.add_trace(i, row=1, col=2)

packet_queue_subplot.update_layout(title_text="Packet Queue probability", xaxis_title="k", yaxis_title="Pk", title_x=0.5, title_font=dict(size=22))


for i in STATIC_RESULTS['packets_plot'].data:
    packet_subplot.add_trace(i, row=1, col=2)
yaxis=dict(range=[0, 10])
packet_subplot.update_layout(title_text="Packet", xaxis_title=unicodeit.replace("\\rho"), yaxis_title="Lq, Ls", yaxis=dict(range=[0, 10]), title_x=0.5, title_font=dict(size=22))

    
for i in STATIC_RESULTS['time_plot'].data:
    time_subplot.add_trace(i, row=1, col=2)

time_subplot.update_layout(title_text="Time",         
                           xaxis_title=unicodeit.replace("\\rho"),  # Use unicode to display the greek letter rho
                           yaxis_title=unicodeit.replace("\\muWs, \\muWq"), 
                           yaxis=dict(range=[0, 10]), 
                           title_x=0.5, 
                           title_font=dict(size=22))


# SIMULATION PLOTS INITIALIZATION #
for i in SIMULATION_RESULTS['packet_queue_plot'].data:
    packet_queue_subplot.add_trace(i, row=1, col=1)
packet_queue_subplot.update_xaxes(title_text="k", row=1, col=2)

for i in SIMULATION_RESULTS['packets_plot'].data:
    packet_subplot.add_trace(i, row=1, col=1)
packet_subplot.update_xaxes(title_text=unicodeit.replace("\\rho"), row=1, col=2)

for i in SIMULATION_RESULTS['time_plot'].data:
    time_subplot.add_trace(i, row=1, col=1)
time_subplot.update_xaxes(title_text=unicodeit.replace("\\rho"), row=1, col=2)


# SHOW PLOTS #
STATIC_RESULTS["packet_distribution"].show()
packet_queue_subplot.show()
packet_subplot.show()
time_subplot.show()
