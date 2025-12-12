# CarScout

CarScout is a small console app to view, search, and add cars stored in a CSV file. This guide walks you through setup and usage with minimal steps.

## What’s inside

- `src/carapp/app.py`: The main program.
- `src/carapp/cars_data.csv`: Sample car data (you can add your own).

## Run the app (simplest way)

```bash
cd <project-folder>
python src/carapp/app.py
```

## Using the menu

- `1 - Show all cars`: Lists every car in `cars_data.csv`.
- `2 - Search car by price`: Enter a max price to see matches.
- `3 - Add a new car`: Enter details; the car is added in memory.
- `4 - Save & Exit`: Writes all cars back to the CSV, then quits.

Important: Data is saved only when you choose **Save & Exit**.

## Where data is stored

- File: `src/carapp/cars_data.csv`.
- The program reads/writes this file relative to where you run it. Run from the project root so you’re using the same file consistently.

## Troubleshooting

- “File not found” or empty data: Ensure you run from the project root so it uses `src/carapp/cars_data.csv`.
- Added cars not saved: Always choose `4 - Save & Exit` before closing.
