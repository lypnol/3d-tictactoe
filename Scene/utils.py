from vpython import vector

def hex_to_color_vector(h):
     return vector(*tuple(int(h[i:i+2], 16) / 256 for i in (0, 2 ,4)))
