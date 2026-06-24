import pandas as pd
import numpy as np
import sqlite3

def run_pipeline():
    try:
        print("Starting the data pipeline..\n")
        
        # step1: loading all the raw data files into pandas Dataframe
        print("step1: Reading CSV files")
        df_sales = pd.read_csv('sales_data.csv')
        df_products = pd.read_csv('products.csv')
        df_stores = pd.read_csv('stores.csv')
        
        print(f"Sales table has{df_sales.shape[0]} rows and {df_sales.shape[1]} columns")
        print("Checking for null values in sales:")
        print(df_sales.isnull().sum(),"\n")
        
        # step 2: Cleaning the data (handling nulls and duplicates)
        print("step 2: Cleaning up the messy data")
        
        # removing duplicate rows to ensure data accuracy
        old_row_count= len(df_sales)
        df_sales= df_sales.drop_duplicates()
        print(f" removed{old_row_count - len(df_sales)} duplicate rows")
        
        # if quantity is missing , filling it with 0
        df_sales['quantity'] = df_sales['quantity'].fillna(0)
        
        # Dropping rows where 'amount' is NUll as they are invalid transactions
        df_sales= df_sales.dropna(subset=['amount'])
        
        # standardizing date format and amount data type
        df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'])
        df_sales['amount']= df_sales['amount'].astype(float)
        print("Data cleaning done.\n")
        
        # Step 3: Joining tables and calculating new metrics
        print("step 3: merging tables to get product and store details")
        
        # using left join to keep all sales records intact even if product/store details are missing
        merge1= pd.merge(df_sales,df_products, on='product_id',how='left')
        final_data = pd.merge(merge1,df_stores, on='store_id',how='left')
        
        #Calculating the new total_revenue column (quantity*price)
        final_data['total_revenue']=final_data['quantity']*final_data['price']
        
        # using Numpy to calculate mathmatical statistics efficiently
        rev_array = final_data['total_revenue'].to_numpy()
        print(f"revenue average is{np.mean(rev_array):.2f}")
        print(f"highest revenue is {np.max(rev_array)} and lowest is{np.min(rev_array)}\n")
        
        # step 4: saving the clean data to a sqlite databse
        print("step 4: Loading data into SQLite database")
        db_conn = sqlite3.connect('retail_database.db')
        
        # saving the dataframe as a sql table, replacing if it already exists
        final_data.to_sql('retail_sales',db_conn,if_exists='replace',index=False)
        print("saved data to 'retail_sales' table successfully!\n")
        
        # step 5: running sql queries for business reporting
        print("step 5: fetching business reports")
        
        #Query 1: Find the top 3 best selling products based on total quantity
        q1="""
        select product_name,sum(quantity) as total_sold
        from retail_sales
        group by product_name
        order by total_sold desc
        limit 3
        """
        print("___Top 3 products___")
        print(pd.read_sql_query(q1, db_conn))
        
        # query2: find total revenue generated per store
        q2="""
        select store_name, sum(total_revenue) as store_revenue
        from retail_sales
        group by store_name
        """
        print("\n Revenue generated per store")
        print(pd.read_sql_query(q2, db_conn))
        
        #closing the database connection to free up resources
        db_conn.close()
        print("\nPipeline finished successfully without errors!")
    
    # handling the case where csv files are missing from the directory
    except FileNotFoundError:
        print("Error: could not find the csv files. please checl if they are in the same folder")
        
    # Catching any other unexpected error to prevent ugly crashes
    except Exception as e:
        print("An unexpected error occured:",e)
    
# Executing the pipeline function
if __name__=="__main__":
    run_pipeline()
        
        
        
        
        
        
        