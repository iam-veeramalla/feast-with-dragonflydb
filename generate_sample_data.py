"""
Generate sample data for the Feast demo
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_user_stats():
    """Generate sample user statistics data"""
    np.random.seed(42)
    
    # Generate data for 100 users
    num_users = 100
    user_ids = list(range(1, num_users + 1))
    
    # Generate timestamps (last 7 days)
    base_time = datetime.now()
    timestamps = [base_time - timedelta(days=i % 7) for i in range(num_users)]
    
    # Generate feature values
    total_orders = np.random.randint(1, 50, size=num_users)
    total_spent = np.random.uniform(10.0, 5000.0, size=num_users)
    avg_order_value = total_spent / total_orders
    
    # Create DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'event_timestamp': timestamps,
        'total_orders': total_orders,
        'total_spent': total_spent.astype(np.float32),
        'avg_order_value': avg_order_value.astype(np.float32),
    })
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to parquet
    output_path = 'data/user_stats.parquet'
    df.to_parquet(output_path, index=False)
    print(f"✅ Generated sample data: {output_path}")
    print(f"   - {len(df)} user records created")
    print(f"\nSample data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    generate_user_stats()
