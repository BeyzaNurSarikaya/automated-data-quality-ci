import pandas as pd
import os
import sys
import requests
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# 1. Hidden Settings 
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

# 2. DATA CREATION (Since the Github file limit is only 25 MB, I'm creating a sample data file.)
def create_sample_data():
    os.makedirs("data", exist_ok=True)
    # Test scenario: 3 valid, 1 invalid (qty: -1) rows
    data = {
        'order_id': ['TXN-101', 'TXN-102', 'TXN-103', 'TXN-104'],
        'qty': [2, 5, -1, 10],  # -1 error will be triggered
        'amount': [150.5, 200.0, 50.0, 300.0],
        'currency': ['INR', 'INR', 'INR', 'INR'],
        'ship_country': ['IN', 'IN', 'IN', 'IN'],
        'date': ['05-01-22', '05-02-22', '05-03-22', '05-04-22']
    }
    pd.DataFrame(data).to_csv("data/amazon_orders.csv", index=False)
    print("✅ Sample data created successfully.")

# 3. PYDANTIC MODEL
class OrderModel(BaseModel):
    order_id: str
    qty: int = Field(ge=0) # The quantity cannot be less than zero.
    amount: float = Field(ge=0)
    currency: str
    ship_country: str

# 4. VALIDATION AND SLACK
def run_validation():
    create_sample_data() 
    df = pd.read_csv("data/amazon_orders.csv")
    
    errors = []
    for _, row in df.iterrows():
        try:
            OrderModel(**row.to_dict())
        except ValidationError as e:
            errors.append(f"Order {row['order_id']} failed: {e.json()}")

    if errors:
        msg = f"🚨 *CI Data Quality Alert!* 🚨\nFound {len(errors)} invalid rows in commit."
        print(msg)
        if SLACK_WEBHOOK:
            requests.post(SLACK_WEBHOOK, json={"text": msg})
        sys.exit(1) # STOPS THE PIPELINE
    else:
        print("✅ All data is valid!")
        sys.exit(0)

if __name__ == "__main__":
    run_validation()
