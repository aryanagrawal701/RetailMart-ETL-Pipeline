# ETL Data Pipeline Assignment

Hello, this is my submission for the Data Engineering technical assignment. I created an ETL pipeline using Python, Pandas, and SQLite to clean and process retail sales data.

## My Logic and Steps

1. **Reading Data:** I loaded the 3 raw CSV files (sales, products, stores) into pandas dataframes. I manually added some duplicate rows and missing values in the dummy data to test my cleaning logic.
2. **Cleaning:** I first removed the duplicate rows. For missing data, if the 'quantity' was missing, I filled it with 0. However, if the 'amount' was missing, I completely dropped that row because a transaction without an amount cannot be used to calculate revenue. 
3. **Merging:** I used a LEFT JOIN to combine the sales data with product and store details. I chose a left join specifically so that no core sales records are lost during the merge, even if product or store IDs are missing.
4. **Database Storage:** I calculated the total revenue (quantity * price) and saved the final clean data into a local SQLite database (`retail_database.db`). I chose SQLite so that anyone checking my code can run it easily without needing to set up a separate SQL server.
5. **Queries:** Finally, I ran SQL queries inside the script to print the top 3 best-selling products and the total revenue per store.

## How to run the code

1. Open your terminal and install the required libraries:
   `pip install pandas numpy`

2. Run the python script:
   `python etl_pipeline.py`

After running, you will see the cleaning process logs and the final business reports in the terminal. The `retail_database.db` file will also be created in the same folder.