"""
Demo script for Feast with Redis online store
"""
import os
import sys
import shutil
from datetime import datetime
from feast import FeatureStore
import pandas as pd

def main():
    print("=" * 60)
    print("🔴 FEAST WITH REDIS DEMO")
    print("=" * 60)
    
    # Change to feature_repo directory
    os.chdir('feature_repo')
    
    # Copy Redis config to feature_store.yaml
    print("\n1️⃣  Setting up Feast with Redis configuration...")
    shutil.copy('feature_store_redis.yaml', 'feature_store.yaml')
    print("✅ Using Redis at localhost:6379")
    
    # Apply feature definitions
    print("\n2️⃣  Applying feature definitions to registry...")
    os.system("feast apply")
    
    # Initialize Feast store
    store = FeatureStore(repo_path=".")
    
    # Materialize features to online store
    print("\n3️⃣  Materializing features to Redis online store...")
    end_date = datetime.now()
    store.materialize(
        start_date=datetime(2025, 10, 1),
        end_date=end_date
    )
    print("✅ Features materialized to Redis")
    
    # Fetch online features
    print("\n4️⃣  Fetching online features from Redis...")
    entity_rows = [
        {"user_id": 1},
        {"user_id": 5},
        {"user_id": 10},
    ]
    
    features = store.get_online_features(
        features=[
            "user_stats:total_orders",
            "user_stats:total_spent",
            "user_stats:avg_order_value",
        ],
        entity_rows=entity_rows,
    ).to_dict()
    
    # Display results
    print("\n📊 Retrieved Features from Redis:")
    print("-" * 60)
    df = pd.DataFrame(features)
    print(df.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("✅ Redis demo completed successfully!")
    print("=" * 60)
    
    # Change back to original directory
    os.chdir('..')

if __name__ == "__main__":
    main()
