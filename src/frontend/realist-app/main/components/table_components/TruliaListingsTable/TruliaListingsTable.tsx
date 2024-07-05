import { AgGridReact } from "ag-grid-react";
import React, { useEffect, useState } from "react";
import { ApiTruliaListingResponse, PriceHistory, TruliaListingFull, TruliaListingSummary } from "../../../helpers/globalInterfaces";
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
import { Box, Flex, Text } from "@chakra-ui/react";
import { ColDef } from "ag-grid-community";
import "../agGridTable.css"

interface TruliaListingsTableProps {
    isFetching: boolean
    listings?: ApiTruliaListingResponse[];

}

export function TruliaListingsTable ({isFetching, listings}: TruliaListingsTableProps){
    console.log('trulialisting table loading', listings)
    const columnsData: ColDef<TruliaListingSummary>[] = [
        { headerName: "Address", field: "address" },
        { headerName: "Neighborhood", field: "neighborhood" },
        { headerName: "Asking Price", field: "askingPrice" },
        { headerName: "Bedrooms", field: "bedrooms" },
        { headerName: "Bathrooms", field: "bathrooms" },
        { headerName: "Floor Sqft", field: "floorSqft" },
        { headerName: "Property Type", field: "propertyType" },
        { headerName: "Year Built", field: "yearBuilt" },
        { headerName: "Date Listed/Sold", field: "dateListedOrSold" },
        { headerName: "Description", field: "description"},
    ]

    const [rowsData, setRowsData] = useState<TruliaListingSummary[]>([])
    
    useEffect(()=>{
        if (listings){
            let listingsSummaryList: TruliaListingSummary[] = []
            for (let listing of listings){
                let listingsFull = convertApiResponseToTruliaListingObject(listing);
                let listingsSummary = summarizeListing(listingsFull);
                listingsSummaryList.push(listingsSummary)
            }
            setRowsData(listingsSummaryList)
        }
    }, [listings])

    const convertApiResponseToTruliaListingObject = (apiListingObject: ApiTruliaListingResponse) => {
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
                        priceChangeValue: apiListingObjectPriceHistory.priceChange.priceChangeValue.formattedPrice
                    } : undefined
                }
                listingObjectPriceHistoryList.push(listingObjectPriceHistory);
            }
        }
        
        let listingFull: TruliaListingFull = {
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
            dateListedOrSold: apiListingObject.date_listed_or_sold,
            architecture: apiListingObject.architecture,
            basement: apiListingObject.basement,
            condition: apiListingObject.condition,
            foundation: apiListingObject.foundation,
            houseMaterial: apiListingObject.house_material,
            structureType: apiListingObject.structure_type,
            lotSqft: apiListingObject.lot_sqft,
            parking: apiListingObject.parking,
            priceHistory: listingObjectPriceHistoryList,
            mlsListingId: apiListingObject.mls_listing_id,
            description: apiListingObject.description,
        }

        return listingFull;
    }

    const summarizeListing = (listing: TruliaListingFull) => {
        let listingSummary: TruliaListingSummary = {
            address: listing.address,
            askingPrice: listing.askingPrice,
            bedrooms: listing.bedrooms,
            bathrooms: listing.bathrooms,
            neighborhood: listing.neighborhood,
            floorSqft: listing.floorSqft,
            propertyType: listing.propertyType,
            yearBuilt: listing.yearBuilt,
            dateListedOrSold: listing.dateListedOrSold,
            description: listing.description
        }
        return listingSummary;
    }


    
    return (
        <Flex width="100%" height="100%" minHeight="250px" className="ag-theme-quartz">
            {   
                (listings !== undefined && !isFetching) 
                    ? <Box width="100%">
                        <AgGridReact
                            columnDefs={columnsData}
                            rowData={rowsData}
                            pagination={true}
                            paginationPageSize={200}
                            paginationPageSizeSelector={[50, 200, 500, 1000]}
                        />
                    </Box>
                    : <Box flex="1" alignSelf="center" justifySelf="center">
                        <Box as="i" className="fa fa-refresh fa-spin fa-10x"/>
                        <Text fontSize="3xl" marginTop="20px">Fetching all data... this may take up to a minute</Text>
                    </Box>       
            }
        </Flex>
        

    )
}
