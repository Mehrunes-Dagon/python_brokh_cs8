import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

from graph import *

graph_data = Graph()
graph_data.create_test_data()
print(graph_data.vertexes)

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

# debug_pallet = Spectral8
# debug_pallet.append('#ff0000')
# debug_pallet.append('#0000ff')

plot = figure(title='Graph Layout Demonstration', x_range=(0, 500), y_range=(0, 500),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Oval(height=10, width=10, fill_color='color')

# this is drawing edges from start to end
graph.edge_renderer.data_source.data = dict(
    # TODO what is happening here???
    # why all edges start from first vertex: is a list of some kind that has to do with strating points
    start=[0]*N,
    end=node_indices)  # is a list of some kind that has to do with ending points
# print(start)
# print(end)

# start of layout code
# circ = [i*2*math.pi/N for i in node_indices]
x = [v.pos['x'] for v in graph_data.vertexes]  # assembling a list
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)
