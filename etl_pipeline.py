import pandas as pd
import numpy as np
import sqlite3

def run_pipeline():
    try:
        print("Starting the data pipeline..\n")
        
        # 1. read csv files
        sales = pd.read_csv('sales_data.csv')
        products = pd.read_csv('products.csv')
        stores = pd.read_csv('stores.csv')
        
        print(f"Sales data shape:{sales.shape}")
        print(sales.head(), "\n")
        
        print(f"Products data shape: {products.shape}")
        print(products.head(), "\n")
        
        print(f"Stores data shape: {stores.shape}")
        print(stores.head(), "\n")
        
        # Check the missing values
        print("Null values in Sales: ")
        print(sales.isnull().sum(), "\n")
        
        print("Null values in Products: ")
        print(products.isnull().sum(), "\n")
        
        print("Null values in Stores: ")
        print(stores.isnull().sum(), "\n")
       
        # 2. clean the data
        initial_rows = len(sales)
        sales= sales.drop_duplicates()
        print(f" removed {initial_rows - len(sales)} duplicate rows")
        
        # fill missing quantity with 0 and drop rows without amount
        sales['quantity'] = sales['quantity'].fillna(0)
        sales= sales.dropna(subset=['amount'])
        print(f"Cleaned sales data shape: {sales.shape}\n")
        
        # fix data type
        sales['sale_date'] = pd.to_datetime(sales['sale_date'])
        sales['amount']= sales['amount'].astype(float)
        
        # 3. merge tables
        sales_prod= pd.merge(sales, products, on='product_id',how='left')
        full_data = pd.merge(sales_prod, stores, on='store_id',how='left')
        print("Final merged table:")
        print(full_data.head(),"\n")
        
        # calculate revenue
        full_data['total_revenue']=full_data['quantity']*full_data['price']
        revenue_vals = full_data['total_revenue'].to_numpy()
    
        print(f"Average revenue is{np.mean(revenue_vals):.2f}")
        print(f"highest revenue is {np.max(revenue_vals)} and lowest is {np.min(revenue_vals)}\n")
        
        # Groupby city and revenue
        city_revenue = full_data.groupby('city')['total_revenue'].sum().reset_index()
        city_revenue = city_revenue.sort_values(by='total_revenue', ascending=False)
        print(city_revenue.to_string(index=False), "\n")
        
        # 4. save to database
        conn = sqlite3.connect('retail_database.db')
        full_data.to_sql('retail_sales',conn,if_exists='replace',index=False)
        
        # print reports
        q1="""
        select product_name,sum(quantity) as total_sold
        from retail_sales
        group by product_name
        order by total_sold desc
        limit 3
        """
        print("---Top 3 products---")
        print(pd.read_sql_query(q1, conn))
        
        q2="""
        select store_name, sum(total_revenue) as store_revenue
        from retail_sales
        group by store_name
        """
        print("\n---store Revenue---")
        print(pd.read_sql_query(q2, conn))
        
        # print summary report
        print("\n" + "="*35)
        print("FINAL SUMMARY REPORT")
        print("="*35)
        
        total_transactions = len(full_data)
        total_revenue_sum = full_data['total_revenue'].sum()
        top_city = full_data.groupby('city')['total_revenue'].sum().idxmax()
        top_product = full_data.groupby('product_name')['quantity'].sum().idxmax()
        
        print(f"Total number of transactions: {total_transactions}")
        print(f"Total revenue: {total_revenue_sum:.2f}")
        print(f"Top selling city: {top_city}")
        print(f"Top selling product: {top_product}")
        print("="*35 + "\n")
        
        conn.close()
        print("\nDone!")
    
    except FileNotFoundError:
        print("Error: could not find the csv files. please checl if they are in the same folder")
    except Exception as e:
        print("An unexpected error occured:",e)
    
if __name__=="__main__":
    run_pipeline()
        
        
        
        
        
        
        