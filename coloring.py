import math
def color(ptile):
    mid_dig = int(255 - min(math.floor(255 * ptile/100), 255))
    mid_hex = format(mid_dig, '02x')
    return '#ff' + mid_hex + '00'
# color(100)  # red
# color(0)    # yellow
