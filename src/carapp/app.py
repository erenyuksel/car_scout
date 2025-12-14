"""Console-based CAR SCOUT application."""

from datetime import datetime

# Path to the CSV file used to persist car records between runs.
DATA_FILE = "cars_data.csv"  # file with car data


# ---------- INPUT VALIDATION ----------

def get_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """Ask user for an integer and (optionally) enforce a min/max range."""
    while True:
        text = input(prompt)
        try:
            value = int(text)

            if min_value is not None and value < min_value:
                print(f"Please enter a number above {min_value}.")
                continue

            if max_value is not None and value > max_value:
                print(f"Please enter a number under {max_value}.")
                continue

            return value
        except ValueError:
            print("Please enter a whole number (e.g. 2018).")



def get_float(prompt: str) -> float:
    """Ask user for a float (number with decimals) and repeat until valid."""
    # Loop forever until a valid float is returned.
    while True:
        # Collect raw user input as text.
        text = input(prompt)
        try:
            # Attempt to convert the input to a float; will raise on bad input.
            value = float(text)  # try convert to float
            # If conversion works, immediately return the numeric value.
            return value
        except ValueError:
            # If conversion fails, inform the user and repeat the loop.
            print("Please enter a number (e.g. 12345.50).")


def get_non_empty_str(prompt: str) -> str:
    """Ask for non-empty text and repeat until something is entered."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("This field cannot be empty. Please enter something.")


def get_transmission(prompt: str = "Transmission (manual/automatic): ") -> str:
    """Ask for transmission type and only accept 'manual' or 'automatic'."""
    while True:
        trans = input(prompt).strip().lower()
        if trans in ("manual", "automatic"):
            return trans
        print("Please type either 'manual' or 'automatic'.")


# ---------- FILE FUNCTIONS ----------

def load_cars() -> list[dict]:
    """
    Read all cars from the file and return a list of dictionaries.
    If the file does not exist, start with an empty list.
    """
    # Prepare an empty list to hold car dictionaries.
    cars: list[dict] = []
    try:
        # Try opening the data file for reading using UTF-8 to handle accents.
        f = open(DATA_FILE, "r", encoding="utf-8")

    except FileNotFoundError:
        # If the file is missing, tell the user and start with no data.
        print("No data file found, starting with empty car list.")
        return cars

    # Iterate over every line in the opened file handle.
    for line in f:
        # Remove any trailing newline or surrounding whitespace.
        line = line.strip()
        # Skip completely empty lines to avoid parsing errors.
        if line == "":
            continue

        # Split the CSV line into its six expected fields.
        b, m, y, km, t, p = line.split(",")

        # Build a dictionary for the current car with typed values.
        car = {
            "brand": b,
            "model": m,
            "year": int(y),
            "km": int(km),
            "trans": t,
            "price": float(p),
        }
        # Append the structured car dictionary to the list.
        cars.append(car)

    # Close the file handle to free system resources.
    f.close()

    # Return the full list of car dictionaries to the caller.
    return cars


def save_cars(cars: list[dict]) -> None:
    """Write all cars back into the file."""
    # Open the CSV file for writing (overwrites existing content).
    f = open(DATA_FILE, "w", encoding="utf-8")
    # Loop over every car dictionary to serialize it.
    for c in cars:
        # Format a CSV line with the six fields in a stable order.
        line = f"{c['brand']},{c['model']},{c['year']},{c['km']},{c['trans']},{c['price']}\n"
        # Write the line to disk.
        f.write(line)
    # Close the file handle after all cars are written.
    f.close()


# ---------- CORE FUNCTIONS ----------

def show_all(cars: list[dict]) -> None:
    """Print all cars."""
    # Header to separate the section in the console.
    print("\n--- ALL CARS ---")
    
    # Iterate through each stored car and print its details on one line.
    for c in cars:
        print(
            c["brand"],
            c["model"],
            "-",
            c["year"],
            "-",
            c["km"],
            "km -",
            c["trans"],
            "- CHF",
            c["price"],
        )


def search_cars(cars: list[dict]) -> None:
    """Find cars under a max price (with validation)."""
    # Ask the user for the highest price they are willing to pay.
    max_price = get_float("Enter max price: ")
    # Intro text before listing matches.
    print("\nCars matching your budget:\n")
    # Track whether any car meets the condition.
    found = False

    # Inspect each car and compare its price to the user's limit.
    for c in cars:
        if c["price"] <= max_price:
            # If within budget, print a short summary and mark as found.
            print(c["brand"], c["model"], "- CHF", c["price"])
            found = True

    # If no car matched the condition, inform the user explicitly.
    if not found:
        print("No cars found for your expected price.")


def add_car(cars: list[dict]) -> None:
    """Add new car to the list (with validation)."""
    # Section header for clarity in the console.
    print("\n--- ADD CAR ---")
    # Gather textual fields directly.
    brand = get_non_empty_str("Brand: ")
    model = get_non_empty_str("Model: ")
    # Collect numeric fields using validators to enforce correct types.
    current_year = datetime.now().year
    year = get_int("Year: ", min_value=1886, max_value=current_year)
    km = get_int("Kilometers: ", min_value=0)
    # Normalize transmission input by trimming spaces and lowering case.
    trans = get_transmission()
    # Gather price as a validated float.
    price = get_float("Price: ")

    # Construct a dictionary representing the new car.
    new_car = {
        "brand": brand,
        "model": model,
        "year": year,
        "km": km,
        "trans": trans,
        "price": price,
    }
    # Store the new car in the in-memory list.
    cars.append(new_car)
    # Confirm to the user that the operation succeeded.
    print("Car added!")


def main() -> None:
    """Main loop with menu."""
    # Greeting shown once when the program starts.
    print("Welcome to CAR SCOUT!\n")
    # Load existing cars from disk into memory.
    cars = load_cars()

    # Run a perpetual menu loop until the user chooses to exit.
    while True:
        # Show the available menu options every cycle.
        print("\n=== CAR SCOUT MENU ===")
        print("1 - Show all cars")
        print("2 - Search car by price")
        print("3 - Add a new car")
        print("4 - Save & Exit")

        # Collect the user's menu selection.
        choice = input("Your choice: ")

        # Dispatch to the correct function based on the choice.
        if choice == "1":
            show_all(cars)
        elif choice == "2":
            search_cars(cars)
        elif choice == "3":
            add_car(cars)
        elif choice == "4":
            # Persist all cars to disk before quitting.
            save_cars(cars)
            # Say goodbye to give clear feedback.
            print("Saved. Goodbye!")
            # Break out of the loop to end the program.
            break
        else:
            # Handle any invalid input by prompting again next loop.
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    # Only run the interactive menu when the module is executed directly.
    main()
