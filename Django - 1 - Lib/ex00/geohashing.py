import sys
from antigravity import geohash


def print_usage():
    print(
        "Usage: python3 geohashing.py <latitude> <longitude> <date-dow>",
        file=sys.stderr,
    )
    print(
        "Example: python3 geohashing.py 37.421542 -122.085589 2005-05-26-10458.68",
        file=sys.stderr,
    )


def validate_date_dow(s):
    if not isinstance(s, str):
        raise ValueError("date-dow must be a string")

    if len(s) < 12:
        raise ValueError("date-dow too short, expected format YYYY-MM-DD-<dow>")

    try:
        if s[4] != "-" or s[7] != "-":
            raise ValueError("date must be in format YYYY-MM-DD")

        year_s = s[0:4]
        month_s = s[5:7]
        day_s = s[8:10]

        if not (year_s.isdigit() and month_s.isdigit() and day_s.isdigit()):
            raise ValueError("date contains non-digit characters")

        _ = int(year_s)
        month = int(month_s)
        day = int(day_s)

        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        if day < 1 or day > 31:
            raise ValueError("day must be in 1..31")

        if len(s) <= 11:
            raise ValueError("missing Dow opening value after date")

        dow_str = s[11:]

        try:
            _ = float(dow_str)
        except ValueError:
            raise ValueError("Dow opening value must be a number (e.g. 10458.68)")

    except IndexError:
        raise ValueError("date-dow has unexpected format")

    return s.encode("utf-8")


def main():
    if len(sys.argv) != 4:
        print("Error: 3 arguments required", file=sys.stderr)
        print_usage()
        sys.exit(1)

    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
    except ValueError as e:
        print(f"Error: invalid coordinate - {e}", file=sys.stderr)
        print_usage()
        sys.exit(1)

    try:
        date_dow = validate_date_dow(sys.argv[3])
    except ValueError as e:
        print(f"Error: invalid date-dow - {e}", file=sys.stderr)
        print_usage()
        sys.exit(1)

    try:
        geohash(lat, lon, date_dow)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
