TRULIA_MAIN_TABLE_COLUMNS = [
    'key', 'location', 'address', 'city', 'state', 'zip',
    'asking_price', 'trulia_url', 'floor_sqft', 'lot_sqft',
    'bedrooms', 'bathrooms', 'basement', 'foundation', 'structure_type',
    'architecture', 'house_material', 'condition', 'mls_listing_id',
    'trulia_listing_id', 'parcel_number', 'date_listed_or_sold',
    'days_on_market', 'listing_status', 'neighborhood', 'property_type',
    'property_subtype', 'parking', 'year_built', 'year_renovated', 'price_history', 'description'
]

TRULIA_MAIN_TABLE_VALUES = f'({", ".join(TRULIA_MAIN_TABLE_COLUMNS)}) VALUES ({", ".join("%(" + col + ")s" for col in TRULIA_MAIN_TABLE_COLUMNS)})'

TRULIA_MAIN_TABLE_NAME = 'trulia_house_listing'