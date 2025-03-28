import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_business_data(num_records=1000):
    products = ["WidgetA", "GadgetB", "ServiceC", "BundleD"]
    regions = ["North", "South", "East", "West", "Online"]
    campaigns = ["SpringSale", "HolidayBlitz", "ReferralProgram", None]
    market_trends = ["Growing", "Stable", "Declining"]

    data = []
    start_date = datetime.now() - timedelta(days=730)

    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 730))
        sales_amount = round(random.uniform(500, 50000), 2)
        operational_cost = round(random.uniform(1000, 15000), 2)
        customer_acq_cost = round(random.uniform(50, 500), 2)
        total_cost = operational_cost + customer_acq_cost
        profit_margin = round((sales_amount - total_cost) / sales_amount, 2)
        
        record = {
            "Date": date.strftime("%Y-%m-%d"),
            "Product": random.choice(products),
            "Region": random.choice(regions),
            "Sales_Amount": sales_amount,
            "Marketing_Campaign": random.choice(campaigns),
            "Customer_ACQ_Cost": customer_acq_cost,
            "Support_Tickets": random.randint(0, 25),
            "Operational_Cost": operational_cost,
            "Profit_Margin": max(0.15, min(0.45, profit_margin)),
            "Market_Trend": random.choice(market_trends)
        }
        data.append(record)

    df = pd.DataFrame(data)
    
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    os.makedirs(samples_dir, exist_ok=True)
    
    output_path = os.path.join(samples_dir, f'business_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    df.to_csv(output_path, index=False)
    print('Done!')
    return df

if __name__ == "__main__":
    generate_business_data()
