
import math

def parse_transit_corridor(corridor_code):

    if not isinstance(corridor_code, str):
        return "Invalid corridor code"

    parts = corridor_code.strip().split('-')

    if len(parts) != 3 or any(not part.strip() for part in parts):
        return "Invalid corridor code"

    orig, dest, zones_str = parts

    try:
        zones = int(zones_str.strip())

        if zones <= 0:
            return "Invalid corridor code"

        base_fare = 2.50 + (zones * 0.75)

        return (
            f"Route {orig.strip().upper()}->{dest.strip().upper()}: "
            f"{zones} Zones, Fare ${base_fare:.2f}"
        )

    except (ValueError, TypeError, OverflowError):
        return "Invalid corridor code"


def lookup_concession_discount(category_name):

    if not isinstance(category_name, str):
        return None

    category = category_name.strip().upper()

    discounts = {
        "STANDARD": 1.00,
        "STUDENT": 0.50,
        "SENIOR": 0.35,
        "MILITARY": 0.20,
        "CHILD": 0.00
    }


    return discounts.get(category)


def compute_passenger_density(occupancy_ratio_str):


    if not isinstance(occupancy_ratio_str, str):
        return "Invalid occupancy ratio"

    parts = occupancy_ratio_str.split('/')


    if len(parts) != 2:
        return "Invalid occupancy ratio"

    try:
        passengers = float(parts[0].strip())
        km = float(parts[1].strip())


        if not math.isfinite(passengers) or not math.isfinite(km):
            return "Invalid occupancy ratio"


        if passengers < 0 or km <= 0:
            return "Invalid occupancy ratio"

        density = passengers / km

        if not math.isfinite(density):
            return "Invalid occupancy ratio"

        return round(density, 2)

    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return "Invalid occupancy ratio"


def main():

    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    print(parse_transit_corridor(c_input))

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    print("Multiplier:", lookup_concession_discount(cat_input))

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    print("Density:", compute_passenger_density(d_input))


if __name__ == "__main__":
    main()
