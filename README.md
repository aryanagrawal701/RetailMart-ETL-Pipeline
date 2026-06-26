# RetailMart ETL Data Pipeline

Hello, This is a simple ETL (Extract, Transform, Load) pipeline project. It takes raw retail data, cleans it up, does some calculations, and saves it into a local database.

## How This Project Works
I write a Python script (etl_pipeline.py) that runs the whole process step-by-step:

1. Extract (Reading Data): First, it reads dummy data from three CSV files (sales_data.csv, products.csv, stores.csv). It also checks the shape of the data and looks for missing values.

2. Transform (Cleaning Data): 
   - It removes duplicate rows.
   - If the quantity is missing, it puts a 0. But if the amount is missing, it drops the row entirely (because we can't calculate revenue without money details).
   - It also fixes the date format and converts the amount to float so the math works properly.

3. Transform (Merging & Calculations): 
   - It joins the three tables together using a LEFT JOIN so we don't lose any original sales data.
   - It calculates the total_revenue (Quantity * Price). 
   - I used NumPy to quickly find the average, highest, and lowest revenue.

4. Load (Saving Data): 
   - It automatically creates a local SQLite database (retail_database.db) and saves all the clean data into a table called retail_sales.

5. Final Reports: 
   - At the very end, it runs SQL queries inside Python to show the top 3 best-selling products. 
   - It also prints a quick summary report on the terminal (total transactions, top city, etc.).

## Tools I Used
* Python: The main language for writing the script.
* Pandas: For reading, cleaning, and joining the tables easily.
* NumPy: For doing fast math calculations on the revenue.
* SQLite3: I used this because it creates a simple local .db file. .

## How to Run It
Make sure you have Python installed, and run `pip install pandas numpy` if you don't have them.
1. Download or clone this folder.
2. Open your terminal inside this folder.
3. Run this command:
   python etl_pipeline.py
4. You will see the step-by-step output on your screen, and a new database file will be created automatically.