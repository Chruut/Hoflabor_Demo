import pandas as pd
import panel as pn
import pyvista as pv
import hvplot.pandas
import vtk
from math import pi
from bokeh.io import show
from bokeh.models import (AnnularWedge, ColumnDataSource, Legend, LegendItem, Plot, Range1d, Label)
if not pn.state.loaded:
    pn.extension('tabulator', 'vtk')
#supplementary packages
#import numpy as np
#from pyvista import examples
#import matplotlib as plt


# Load the data into a DataFrame format  
if 'data' not in pn.state.cache.keys():

    df = pd.read_csv('zoo_data.csv')

    pn.state.cache['data'] = df.copy()

else: 

    df = pn.state.cache['data']


# Display the DataFrame    
#print(df.head())
idf = df.interactive() # Make Dataframe interactive


######################################### PLOTS AND TABLES ################################################

##### 1. Plot: Creating a 3D field overview
plotter = pv.Plotter() # we define a pyvista plotter

# Add a Range Slider for field selection
feld_slider = pn.widgets.IntRangeSlider(name='Feldauswahl', start=1, end=5, value=(1, 4), step=1,width=600)

## Protperties of our boxes
# Soil layer
outer_bounds = [0, 5, 0, 3, 0, 0.5]
x_start, x_end = 0, 4
inner_bounds = [x_start, x_end, -0.01, 3.1, -0.01, 0.51]
outer_box = pv.Box(bounds=outer_bounds,level=4)
inner_box = pv.Box(bounds=inner_bounds,level=2)
plotter.add_mesh(outer_box, style='wireframe', color='green')
soil_actor = plotter.add_mesh(inner_box, style='surface', color='brown')

# Plant layer
carrot_bounds = [0.03,0.97,0.1,2.9,0.57,1]
carrot_box = pv.Box(bounds=carrot_bounds,level=0)
brotato_bounds = [1.03,1.97,0.1,2.9,0.57,1]
brotato_box = pv.Box(bounds=brotato_bounds,level=0)
hemp_bounds = [2.03,2.97,0.1,2.9,0.57,1]
hemp_box = pv.Box(bounds=hemp_bounds,level=0)
pastinaken_bounds = [3.03,3.97,0.1,2.9,0.57,1]
pastinaken_box = pv.Box(bounds=pastinaken_bounds,level=0)
carrot_bounds2 = [4.03,4.97,0.1,2.9,0.57,1]
carrot_box2 = pv.Box(bounds=carrot_bounds2,level=0)

carrot_actor = plotter.add_mesh(carrot_box, style='surface', color='#34344a')
brotato_actor = plotter.add_mesh(brotato_box, style='surface', color='#80475e')
hemp_actor = plotter.add_mesh(hemp_box, style='surface', color='darkgreen')
pastinaken_actor = plotter.add_mesh(pastinaken_box, style='surface', color='#c89b7b')
carrot_actor2 = plotter.add_mesh(carrot_box2, style='surface', color='#34344a')
plotter.remove_actor(carrot_actor2)
carrot_actor2 = None

plotter.camera_position = [
    (2.5, -3, 5),  # Camera location: above and slightly off-center
    (2.5, 1.5, 0.25),  # Focus point: center of the box
    (0, 0, 1)  # View up direction (ensures correct orientation)
]

# To integrate the pyvista plot into a panel layout and use it inside pn.Row(), you need to wrap the pyvista 
# plotter output as a panel object.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
feld_pv = pn.panel(plotter.ren_win,height=160,width=600) 
# Potential shorter alternative:
#vtk_panel = pn.pane.VTK(plotter.ren_win, sizing_mode='stretch_both') # didn't work for me 

##### A Function to update the box when the slider moves
def update_box(event):
    global soil_actor, carrot_actor, brotato_actor, pastinaken_actor, carrot_actor2
    global hemp_actor, hemp_box
    x_start = (event.new[0] - 1)  # Scale slider value to match x_start
    x_end = (event.new[1] )     # Scale slider value to match x_end

    # Growth of carrots
    if (x_start == 0 and x_end >= 1) and carrot_actor is None:
        carrot_actor = plotter.add_mesh(carrot_box, style='surface', color='#34344a')
    # Check if the carrot box should be removed
    elif (x_start > 0 or x_end < 1) and carrot_actor is not None:
        plotter.remove_actor(carrot_actor)
        carrot_actor = None  # Set carrot_actor to None after removing it!
    
    # Growth of potatos    
    if (x_start <= 1 and x_end >= 2) and brotato_actor is None:
        brotato_actor = plotter.add_mesh(brotato_box, style='surface', color='#80475e')
    # Check if the potato box should be removed
    elif (x_start > 1 or x_end < 2) and brotato_actor is not None:
        plotter.remove_actor(brotato_actor)
        brotato_actor = None  # Set brotato_actor to None after removing it!

    if (x_start <= 2 and x_end >= 3) and hemp_actor is None:
        hemp_actor = plotter.add_mesh(hemp_box, style='surface', color='darkgreen')
    # Check if the hemp box should be removed
    elif (x_start > 2 or x_end < 3) and hemp_actor is not None:
        plotter.remove_actor(hemp_actor)
        hemp_actor = None  # Set hemp_actor to None after removing it

    if (x_start <= 3 and x_end >= 4) and pastinaken_actor is None:
        pastinaken_actor = plotter.add_mesh(pastinaken_box, style='surface', color='#c89b7b')
    # Check if the pastinaken box should be removed
    elif (x_start > 3 or x_end < 4) and pastinaken_actor is not None:
        plotter.remove_actor(pastinaken_actor)
        pastinaken_actor = None  # Set pastinaken_actor to None after removing it
        
    if (x_start <= 4 and x_end >= 5) and carrot_actor2 is None:
        carrot_actor2 = plotter.add_mesh(carrot_box2, style='surface', color='#34344a')
    # Check if the carrot box 2 should be removed
    elif (x_start > 4 or x_end < 5) and carrot_actor2 is not None:
        plotter.remove_actor(carrot_actor2)
        carrot_actor2 = None  # Set carrot_actor2 to None after removing it
        
                
    # Update soil box bounds to change its size
    new_inner_bounds = [x_start, x_end, -0.01, 3.1, -0.01, 0.51]
    new_inner_box = pv.Box(bounds=new_inner_bounds, level=2)

    # Remove only the solid soil box
    plotter.remove_actor(soil_actor)
     # Add updated soil box and store the new actor
    soil_actor = plotter.add_mesh(new_inner_box, style='surface', color='brown')
    # Trigger VTK panel update
    feld_pv.param.trigger('object')    


# Link slider to update function and the plot
feld_slider.param.watch(update_box, 'value')


##### 2. Plot: Temperature and Humidity Measurements over a year

# Add a slider
month_slider = pn.widgets.IntSlider(name='Monat', start=1, end=12, step=1, value=12)


# Add a Radiobutton to change display mode of a Graph
yaxis_measure = pn.widgets.RadioButtonGroup(
    name='Messdaten', 
    options=['Temperatur', 'Feuchtigkeit',],
    button_type='success'
)


# Pipeline to use daily average data for plots, grouped by crop type
aggregation_pipeline_by_day = (
    idf
    .groupby(['Jahrestag','Feldtyp'])[['Temperatur','Feuchtigkeit']]
    .mean().round(2)  
    .reset_index()
)

##### Creating 2. Plot 
idf_plot = aggregation_pipeline_by_day.hvplot(x = 'Jahrestag', by='Feldtyp', y=yaxis_measure, line_width=1.3,alpha=0.7, title="Messungen auf Anbauflächen",height=250,width=600).opts(toolbar=None)

##### Creating 3. Plot (Data table)
# Filter data based on slider
idf_pipeline = idf[idf.Monat == month_slider]
# Create the Table
idf_table = idf_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size = 50, width= 600, sizing_mode='stretch_height') 


##### 3. Plot: Donutgraph of cummulated Diversity-Index for each Field  

# Start with Data pipeline/aggregation by field type
aggregation_pipeline_by_day_2 = (
    df
    .groupby(['Feldtyp'])[['Diversitaets-Index']]
    .mean().astype(int)  
    .reset_index()    
)

# Adding a color scheme
aggregation_pipeline_by_day_2['color'] = ['#34344a','#80475e','darkgreen','#c89b7b']

############################ Visual preparation of the plot ###########################
#######################################################################################################
# Normalize share
aggregation_pipeline_by_day_2["Share"] = aggregation_pipeline_by_day_2["Diversitaets-Index"] / aggregation_pipeline_by_day_2["Diversitaets-Index"].sum() * 100
# Compute angles for wedges
aggregation_pipeline_by_day_2["angle"] = aggregation_pipeline_by_day_2["Share"].map(lambda x: 2 * pi * (x / 100)).cumsum()
xdr = Range1d(start=-2, end=2)
ydr = Range1d(start=-2, end=2)
plot = Plot(x_range=xdr, y_range=ydr,width=290,height=290)
plot.title.text = "Diversitätsindex nach Feldtyp"
plot.toolbar_location = None
# Create ColumnDataSource
browsers_source = ColumnDataSource(dict(
    start=[0] + aggregation_pipeline_by_day_2["angle"][:-1].tolist(),
    end=aggregation_pipeline_by_day_2["angle"].tolist(),
    colors=aggregation_pipeline_by_day_2["color"].tolist(),
))
# Add wedges
glyph = AnnularWedge(x=0, y=0, inner_radius=0.9, outer_radius=1.7,
                     start_angle="start", end_angle="end",
                     line_color="white", line_width=3, fill_color="colors")
r = plot.add_glyph(browsers_source, glyph)
# Add legend
legend = Legend(location="center")
for i, name in enumerate(aggregation_pipeline_by_day_2["Feldtyp"]):
    legend.items.append(LegendItem(label=name, renderers=[r], index=i))

plot.add_layout(legend, "center")
plot.legend.background_fill_alpha = 0
plot.legend.border_line_alpha = 0
plot.legend.spacing = 1  # Set the distance between the legend items
################################################################################################

# Wrap plot in Panel
donut_diversity = pn.pane.Bokeh(plot,sizing_mode="fixed")

# Overall Dashboard layout using the "FastList Template"
template = pn.template.FastListTemplate(
    title='Felddaten Dashboard', 
    sidebar=[pn.pane.PNG('Hoflabor_logo.png', sizing_mode='scale_both'),
             pn.pane.Markdown("## Übersicht Temperatur und Bodenfeuchtigkeit am Boden der Anbaustreifen"), 
             pn.layout.Spacer(height=50),
             donut_diversity],
    main=[pn.Row(pn.Column(pn.pane.Markdown("## Auswahl der Mosaikfläche"),feld_slider,feld_pv,   
             idf_plot), pn.Column(pn.pane.Markdown("## Rohdaten der Messungen an Mosaik-Streifen"),idf_table))],
     
    accent_base_color="#88d8b0",
    header_background="forestgreen",   
)

# Serve the Plate
template.servable()



