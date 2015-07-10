def new_matrix(width, height, value):
    return [[value for i in range(height)] for j in range(width)]

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))
