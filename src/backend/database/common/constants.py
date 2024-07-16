from backend.helpers.database_helpers import build_dynamic_update_query_template

TRULIA_MAIN_TABLE_COLUMNS = {
    'key': {'setToNullOnNonUpdate': False},
    'location': {'setToNullOnNonUpdate': False},
    'address': {'setToNullOnNonUpdate': False},
    'city': {'setToNullOnNonUpdate': False},
    'state': {'setToNullOnNonUpdate': False},
    'zip': {'setToNullOnNonUpdate': False},
    'asking_price': {'setToNullOnNonUpdate': False},
    'trulia_url': {'setToNullOnNonUpdate': False},
    'floor_sqft': {'setToNullOnNonUpdate': False},
    'lot_sqft': {'setToNullOnNonUpdate': False},
    'bedrooms': {'setToNullOnNonUpdate': False},
    'bathrooms': {'setToNullOnNonUpdate': False},
    'basement': {'setToNullOnNonUpdate': False},
    'foundation': {'setToNullOnNonUpdate': False},
    'structure_type': {'setToNullOnNonUpdate': False},
    'architecture': {'setToNullOnNonUpdate': False},
    'house_material': {'setToNullOnNonUpdate': False},
    'condition': {'setToNullOnNonUpdate': False},
    'mls_listing_id': {'setToNullOnNonUpdate': True},
    'trulia_listing_id': {'setToNullOnNonUpdate': True},
    'parcel_number': {'setToNullOnNonUpdate': False},
    'date_listed_or_sold': {'setToNullOnNonUpdate': True},
    'days_on_market': {'setToNullOnNonUpdate': True},
    'listing_status': {'setToNullOnNonUpdate': True},
    'neighborhood': {'setToNullOnNonUpdate': False},
    'property_type': {'setToNullOnNonUpdate': False},
    'property_subtype': {'setToNullOnNonUpdate': False},
    'parking': {'setToNullOnNonUpdate': False},
    'year_built': {'setToNullOnNonUpdate': False},
    'year_renovated': {'setToNullOnNonUpdate': False},
    'price_history': {'setToNullOnNonUpdate': False},
    'description': {'setToNullOnNonUpdate': False}
}


COLUMNS = ', '.join(TRULIA_MAIN_TABLE_COLUMNS.keys())
VALUE_PLACEHOLDERS = ', '.join(f"%({col})s" for col in TRULIA_MAIN_TABLE_COLUMNS.keys())
TRULIA_MAIN_TABLE_VALUES = f'({COLUMNS}) VALUES ({VALUE_PLACEHOLDERS})'

TRULIA_MAIN_TABLE_NAME = 'trulia_house_listing'
USERS_DETAIL_TABLE_NAME = 'details'

TRULIA_UPDATE_QUERY = build_dynamic_update_query_template(
    dataColumns=TRULIA_MAIN_TABLE_COLUMNS,
    keyName='key'
)

PHILADELPHIA_ZIP_CODES = [
    '19019', '19102', '19103', '19104', '19105', '19106', '19107', '19108', '19109',
    '19110', '19111', '19112', '19114', '19115', '19116', '19118', '19119', '19120', '19121',
    '19122', '19123', '19124', '19125', '19126', '19127', '19128', '19129', '19130', '19131',
    '19132', '19133', '19134', '19135', '19136', '19137', '19138', '19139', '19140', '19141',
    '19142', '19143', '19144', '19145', '19146', '19147', '19148', '19149', '19150', '19151',
    '19152', '19153', '19154', '19160'
]
