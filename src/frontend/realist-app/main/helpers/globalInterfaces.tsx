export interface ApiSuccessResponse {
    data?: any;
    message: string;
    status: number;
    success: true;
}

export interface ApiFailureResponse {
    message?: string;
    status: number;
    success: false;
}

export interface ApiTruliaListingResponse {
    address: string;
    architecture: string | null;
    asking_price: number;
    basement: string | null;
    bathrooms: string | null;
    bedrooms: string | null;
    city: string | null;
    condition: string | null;
    date_listed_or_sold: string | null;
    date_scraped: string;
    description: string | null;
    floor_sqft: number | null;
    foundation: string | null;
    house_material: string | null;
    key: string;
    latitude: number | null;
    listing_status: string | null;
    location: string | null;
    longitude: number | null;
    lot_sqft: number | null;
    mls_listing_id: string | null;
    neighborhood: string | null; 
    parcel_number: string | null;
    parking: string | null;
    price_history: ApiPriceHistory[] | null;
    property_subtype: string | null;
    property_type: string | null;
    state: string | null;
    structure_type: string | null;
    trulia_listing_id: string | null;
    trulia_url: string | null;
    year_built: number | null;
    year_renovated: number | null;
    zip: string | null;
}

export interface ApiPriceHistory {
    event: string;
    formattedDate: string;
    price: {
        formattedPrice: string;
        formattedPriceAbb: string
    } | null;
    priceChange?: {
        formattedPriceChangePercent: string;
        priceChangeDirection: string;
        priceChangePercent: number;
        priceChangeValue?: {
            formattedPrice: string;
        }
    }
}


export interface UserData {
    username: string;
    id: number;
    isAdmin: boolean;
}

export interface TruliaListingSummary{
    key: string;
    address: string;
    askingPrice: number;
    bedrooms: string | null;
    bathrooms: string | null;
    neighborhood: string | null;
    floorSqft: number | null;
    propertyType: string | null;
    yearBuilt: number | null;
    dateListedOrSold: string | null;
    dateScraped: string;
    description: string | null;
}

export interface TruliaListingFull{
    key: string;
    address: string;
    askingPrice: number;
    bedrooms: string | null;
    bathrooms: string | null;
    neighborhood: string | null;
    city: string | null;
    zip: string | null;
    floorSqft: number | null;
    propertyType: string | null;
    propertySubType: string | null;
    yearBuilt: number | null;
    yearRenovated: number | null;
    dateListedOrSold: string | null;
    dateScraped: string;
    architecture: string | null;
    basement: string | null;
    condition: string | null;
    foundation: string| null;
    houseMaterial: string | null;
    structureType: string | null;
    lotSqft: number | null;
    latitude: number | null;
    longitude: number | null;
    parking: string | null;
    trulia_url: string | null;
    priceHistory: PriceHistory[] | null;
    mlsListingId: string | null;
    description: string | null;
}

export interface PriceHistory {
    event: string;
    formattedDate: string;
    formattedPrice?: string | null;
    priceChange?: {
        formattedPriceChangePercent: string;
        priceChangeDirection: string;
        priceChangePercent: number;
        priceChangeValue?: string;
    }
}

export interface TruliaListingModalOverview {
    askingPrice: number | string;
    bedrooms: string | null;
    bathrooms: string | null;
    neighborhood: string | null;
    floorSqft: number | null;
    lotSqft: number | null;
    propertyType: string | null;
    propertySubType: string | null;
    yearBuilt: number | null;
    yearRenovated: number | null;
    condition: string | null;
}

export interface TruliaListingModalAdditionalInfo {
    dateListedOrSold: string | null;
    architecture: string | null;
    basement: string | null;
    foundation: string| null;
    houseMaterial: string | null;
    structureType: string | null;
    parking: string | null;
}