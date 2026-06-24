# RetailMart ETL Pipeline 

Hello! This is my submission for the Data Engineering technical assignment. I have built a local ETL (Extract, Transform, Load) data pipeline using Python, Pandas, and SQLite.

## Project Structure
To test the pipeline, I manually created three dummy dataset files (`sales_data.csv`, `products.csv`, and `stores.csv`) with 15 rows of data. I intentionally added some duplicate rows and missing values (NULLs) to properly demonstrate the data cleaning process.

## My Approach & Logic
Here is the step-by-step breakdown of how my code works:

1. **Extract (Data Ingestion):** I used the Pandas library to read the raw CSV files into dataframes.

2. **Transform (Data Cleaning):** - I used `drop_duplicates()` to remove duplicate entries based on identical rows.
   - For missing data: If the 'quantity' was missing, I replaced it with 0 using `fillna(0)`. However, if the 'amount' was missing, I completely dropped that row using `dropna()`, because a transaction without an amount is not useful for business calculations.
   - I fixed data types (converting dates to datetime and amounts to float).
   - I used a `LEFT JOIN` to merge the sales data with product and store details so that no sales records get lost during the merge.
   - Finally, I created a new column called `total_revenue` (quantity * price).

3. **Load (Database Storage):** Instead of just saving another CSV, I used Python's built-in `sqlite3` library to create a local database file (`retail_database.db`) and loaded the clean dataframe into a SQL table named `retail_sales`.

4. **Reporting:** At the very end of the script, I wrote actual SQL queries to fetch the Top 3 best-selling products and the total revenue generated per store, which prints directly to the console.

## How to Run My Code
1. Please make sure you have the required libraries installed. You can install them by running:
   `pip install pandas numpy`
2. Run the main script from your terminal:
   `python etl_pipeline.py`
3. The terminal will display the cleaning steps and final reports. You will also see a new `retail_database.db` file created in your folder.