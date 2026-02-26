import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_financial_mockup(num_records=1000000, output_dir=None):
    """
    สร้างข้อมูลจำลองการทำธุรกรรมทางการเงินและบันทึกลงใน Directory ที่กำหนด
    """
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    currencies = ['USD', 'JPY', 'EUR', 'AUD', 'GBP', 'THB', 'CAD', 'SGD']
    items = ['Mega Box', 'Gold Pass', 'Gem Pack (Small)', 'Gem Pack (Large)', 'Hero Skin', 'Resource Bundle']
    exchange_rates = {
        'USD': 1.0, 'JPY': 0.0067, 'EUR': 1.08, 'AUD': 0.65, 
        'GBP': 1.27, 'THB': 0.028, 'CAD': 0.74, 'SGD': 0.74
    }

    data = []
    start_date = datetime(2024, 5, 1)

    for i in range(num_records):
        sc_id = f"SC-{random.randint(100000, 999999)}"
        item = random.choice(items)
        currency = random.choice(currencies)
        base_price = random.choice([0.99, 4.99, 9.99, 19.99, 49.99, 99.99])
        
        amount = round(base_price / exchange_rates[currency], 2)
        if currency == 'JPY':
            amount = round(amount, -1)

        date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        data.append({
            'transaction_id': f"TXN-{1000000 + i}",
            'supercell_id': sc_id,
            'item_name': item,
            'amount_local': amount,
            'currency': currency,
            'timestamp': date
        })

    df = pd.DataFrame(data)
    
    # เพิ่ม Logic การคำนวณ USD ทันที
    df['exchange_rate_to_usd'] = df['currency'].map(exchange_rates)
    df['amount_usd'] = (df['amount_local'] * df['exchange_rate_to_usd']).round(2)

    # จัดการเรื่อง Path และการบันทึกไฟล์
    if output_dir is None:
        # ย้อนกลับไป 1 ระดับจาก src/ แล้วเข้าสู่ data/samples
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_path, 'data', 'samples')

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'financial_mockup_data.csv')
    
    df.to_csv(file_path, index=False)
    print(f"✨ Mockup data generated successfully at: {file_path}")
    return df

if __name__ == "__main__":
    generate_financial_mockup()