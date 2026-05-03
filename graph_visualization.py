from IPython.display import Image, display_png
from graph.workflow import build_graph

img=build_graph().get_graph().draw_ascii()
print(img)