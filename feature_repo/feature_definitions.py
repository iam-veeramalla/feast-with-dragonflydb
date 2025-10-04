from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Define an entity (user)
user = Entity(
    name="user_id",
    description="User identifier",
)

# Define a data source (using parquet file for simplicity)
user_stats_source = FileSource(
    path="../data/user_stats.parquet",
    timestamp_field="event_timestamp",
)

# Define a feature view
user_stats_fv = FeatureView(
    name="user_stats",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="total_spent", dtype=Float32),
        Field(name="avg_order_value", dtype=Float32),
    ],
    source=user_stats_source,
    online=True,
)
