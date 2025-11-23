from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2 +
        cos(radians(lat1)) * cos(radians(lat2)) *
        sin(d_lon / 2) ** 2
    )
    c = atan2(sqrt(a), sqrt(1 - a))

    return R * 2 * c
