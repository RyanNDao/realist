import { format } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';
import { ApiTruliaListingResponse, PriceHistory, TruliaListingFull, TruliaListingSummary } from './globalInterfaces';

export function convertToMap(data: Object): Map<string, any> {
    const map = new Map<string, any>();
    Object.keys(data).forEach(key => {
        map.set(key, data[key]);
    });
    return map;
}

export function formatDbDate(dateString: string, timezone: string  = 'GMT'){ 
    let dateObject = new Date(dateString)
    const dateInTimezone = toZonedTime(dateObject, timezone);
    return format(dateInTimezone, 'yyyy-MM-dd');
}

export function formatCamelCase(inputString: string){
    const spaced = inputString.replace(/([A-Z])/g, ' $1').trim();
    return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

export function formatNumberToMoney(inputNumber: number){
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    });
    return formatter.format(inputNumber);
}

export const convertApiResponseToTruliaListingObject = (apiListingObject: ApiTruliaListingResponse) => {
    let listingObjectPriceHistoryList: PriceHistory[] = [];
    if (apiListingObject.price_history){
        for (let apiListingObjectPriceHistory of apiListingObject.price_history) {
            let listingObjectPriceHistory: PriceHistory = {
                event: apiListingObjectPriceHistory.event,
                formattedDate: apiListingObjectPriceHistory.formattedDate,
                formattedPrice: apiListingObjectPriceHistory.price?.formattedPrice,
                priceChange: apiListingObjectPriceHistory.priceChange ? {
                    formattedPriceChangePercent: apiListingObjectPriceHistory.priceChange.formattedPriceChangePercent,
                    priceChangeDirection: apiListingObjectPriceHistory.priceChange.priceChangeDirection,
                    priceChangePercent: apiListingObjectPriceHistory.priceChange.priceChangePercent,
                    priceChangeValue: apiListingObjectPriceHistory.priceChange.priceChangeValue?.formattedPrice
                } : undefined
            }
            listingObjectPriceHistoryList.push(listingObjectPriceHistory);
        }
    }
    
    let listingFull: TruliaListingFull = {
        key: apiListingObject.key,
        address: apiListingObject.address,
        askingPrice: apiListingObject.asking_price,
        bedrooms: apiListingObject.bedrooms,
        bathrooms: apiListingObject.bathrooms,
        neighborhood: apiListingObject.neighborhood,
        city: apiListingObject.city,
        zip: apiListingObject.zip,
        floorSqft: apiListingObject.floor_sqft,
        propertyType: apiListingObject.property_type,
        propertySubType: apiListingObject.property_subtype,
        yearBuilt: apiListingObject.year_built,
        yearRenovated: apiListingObject.year_renovated,
        dateListedOrSold: apiListingObject.date_listed_or_sold ? formatDbDate(apiListingObject.date_listed_or_sold) : null,
        dateScraped: formatDbDate(apiListingObject.date_scraped),
        architecture: apiListingObject.architecture,
        basement: apiListingObject.basement,
        condition: apiListingObject.condition,
        foundation: apiListingObject.foundation,
        houseMaterial: apiListingObject.house_material,
        structureType: apiListingObject.structure_type,
        longitude: apiListingObject.longitude,
        latitude: apiListingObject.latitude,
        lotSqft: apiListingObject.lot_sqft,
        parking: apiListingObject.parking,
        trulia_url: apiListingObject.trulia_url,
        priceHistory: listingObjectPriceHistoryList,
        mlsListingId: apiListingObject.mls_listing_id,
        description: apiListingObject.description,
    }

    return listingFull;
}

export const returnTruliaFullAndSummaryListFromApiTruliaResponse = (apiTruliaListingResponses: ApiTruliaListingResponse[]) => {
    let listingsSummaryList: TruliaListingSummary[] = []
    let listingsFullList: TruliaListingFull[] = []
    for (let listing of apiTruliaListingResponses){
        let listingsFull = convertApiResponseToTruliaListingObject(listing);
        listingsFullList.push(listingsFull)
        let listingsSummary = convertTruliaFullObjectToTruliaSummaryObject(listingsFull);
        listingsSummaryList.push(listingsSummary)
    }
    return {listingsSummaryList, listingsFullList}
}

export const convertTruliaFullObjectToTruliaSummaryObject = (listing: TruliaListingFull) => {
    let listingSummary: TruliaListingSummary = {
        key: listing.key,
        address: listing.address,
        askingPrice: listing.askingPrice,
        bedrooms: listing.bedrooms,
        bathrooms: listing.bathrooms,
        neighborhood: listing.neighborhood,
        floorSqft: listing.floorSqft,
        propertyType: listing.propertyType,
        yearBuilt: listing.yearBuilt,
        dateListedOrSold: listing.dateListedOrSold,
        dateScraped: listing.dateScraped,
        description: listing.description
    }
    return listingSummary;
}