import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

zone_df = pd.read_csv("/Users/admin/Desktop/Softeer_DE/missions/W4/M2/spark-data/taxi_zone_lookup.csv")

geolocator = Nominatim(user_agent="geoapi")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=3)

def get_coordinates(row):
    location = geocode(f"{row['Zone']}, {row['Borough']}, New York")
    if location:
        return pd.Series([location.latitude, location.longitude])
    else:
        return pd.Series([40.7128, -74.0060])

zone_df[['latitude', 'longitude']] = zone_df.apply(get_coordinates, axis=1)

# Spark에서 쓸 수 있도록 저장
zone_df.to_parquet("/Users/admin/Desktop/Softeer_DE/missions/W4/M2/spark-data/zone_with_coords.parquet", index=False)