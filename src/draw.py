import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Ellipse, ColumnDataSource, Range1d, LabelSet, Label
from bokeh.palettes import Spectral8

from graph import *

# only works as square rn
WIDTH = 600
HEIGHT = 600
CIRCLE_SIZE = 40

graph_data = Graph()
graph_data.create_test_data()
# print(graph_data.vertexes)

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

# debug_pallet = Spectral8
# debug_pallet.append('#ff0000')
# debug_pallet.append('#0000ff')

# TODO: make rectangle, rect?
plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Ellipse(
    height=CIRCLE_SIZE, width=CIRCLE_SIZE, fill_color='color')

start_indices = []
end_indices = []

for start_index, vertex in enumerate(graph_data.vertexes):
    for e in vertex.edges:
        start_indices.append(start_index)
        end_indices.append(graph_data.vertexes.index(e.destination))

graph.edge_renderer.data_source.data = dict(
    start=start_indices,
    end=end_indices)

# TODO: test with this code
# graph.edge_renderer.data_source.data = dict(
#     start=node_indices,  # list of vertexes to start
#     end=list(map(lambda x: x + 1, node_indices)))  # to end

# start of layout code
# circ = [i*2*math.pi/N for i in node_indices]
x = [v.pos['x'] for v in graph_data.vertexes]  # assembling a list
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

# TODO: we run through this loop three times, wtf
value = [v.value for v in graph_data.vertexes]

label_source = ColumnDataSource(data=dict(
    x=x,
    y=y,
    v=value
))

labels = LabelSet(x='x',
                  y='y',
                  text='v',
                  level='overlay',
                  text_align='center',
                  text_baseline='middle',
                  source=label_source,
                  render_mode='canvas')

# investigate plot.add_layout vs plot.renderers.append
plot.add_layout(labels)

output_file('graph.html')
show(plot)
