"""
Optional: Compare performance between Redis and DragonflyDB
"""
import os
import shutil
import time
from datetime import datetime
from feast import FeatureStore
import pandas as pd

def benchmark_feature_retrieval(store, store_name, num_requests=100):
    """Benchmark feature retrieval performance"""
    print(f"\n⏱️  Benchmarking {store_name}...")
    
    entity_rows = [{"user_id": i % 100 + 1} for i in range(num_requests)]
    
    start_time = time.time()
    
    features = store.get_online_features(
        features=[
            "user_stats:total_orders",
            "user_stats:total_spent",
            "user_stats:avg_order_value",
        ],
        entity_rows=entity_rows,
    )
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"   Requests: {num_requests}")
    print(f"   Time: {elapsed:.4f} seconds")
    print(f"   Avg: {(elapsed/num_requests)*1000:.2f} ms per request")
    
    return elapsed

def main():
    print("=" * 60)
    print("📊 PERFORMANCE COMPARISON: REDIS VS DRAGONFLYDB")
    print("=" * 60)
    
    os.chdir('feature_repo')
    
    # Benchmark Redis
    print("\n🔴 Testing Redis...")
    shutil.copy('feature_store_redis.yaml', 'feature_store.yaml')
    redis_store = FeatureStore(repo_path=".")
    redis_time = benchmark_feature_retrieval(redis_store, "Redis", num_requests=100)
    
    # Benchmark DragonflyDB
    print("\n🐉 Testing DragonflyDB...")
    shutil.copy('feature_store_dragonfly.yaml', 'feature_store.yaml')
    dragonfly_store = FeatureStore(repo_path=".")
    dragonfly_time = benchmark_feature_retrieval(dragonfly_store, "DragonflyDB", num_requests=100)
    
    # Compare results
    print("\n" + "=" * 60)
    print("📈 RESULTS")
    print("=" * 60)
    print(f"Redis:       {redis_time:.4f} seconds")
    print(f"DragonflyDB: {dragonfly_time:.4f} seconds")
    
    if dragonfly_time < redis_time:
        improvement = ((redis_time - dragonfly_time) / redis_time) * 100
        print(f"\n🚀 DragonflyDB is {improvement:.1f}% faster!")
    else:
        print(f"\n⚡ Performance is comparable!")
    
    print("\n💡 Note: Results may vary based on system resources and load.")
    
    os.chdir('..')

if __name__ == "__main__":
    main()
