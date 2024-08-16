import { AgGridReact } from "ag-grid-react";
import React, { useEffect, useState } from "react";
import { ApiTruliaListingResponse, PriceHistory, TruliaListingFull, TruliaListingSummary } from "../../../helpers/globalInterfaces";
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
import { Box, Flex, Text } from "@chakra-ui/react";
import { ColDef } from "ag-grid-community";
import "../agGridTable.css"
import { formatNumberToMoney, returnTruliaFullAndSummaryListFromApiTruliaResponse } from "../../../helpers/common";

interface TruliaDataTableProps {
    isFetching: boolean
    onListingClick: any;
    listings?: ApiTruliaListingResponse[];
}

export function TruliaDataTable ({isFetching, onListingClick, listings}: TruliaDataTableProps){
    
    
    console.log('trulialisting table loading', listings)
    const columnsData: ColDef<TruliaListingSummary>[] = [
        { headerName: "Address", field: "address" },
        { headerName: "Neighborhood", field: "neighborhood" },
        { headerName: "Asking Price", field: "askingPrice", valueFormatter: (listing) => formatNumberToMoney(listing.value) },
        { headerName: "Bedrooms", field: "bedrooms" },
        { headerName: "Bathrooms", field: "bathrooms" },
        { headerName: "Floor Sqft", field: "floorSqft" },
        { headerName: "Property Type", field: "propertyType" },
        { headerName: "Year Built", field: "yearBuilt" },
        { headerName: "Date Listed/Sold", field: "dateListedOrSold" },
        { headerName: "Date Scraped", field: "dateScraped" },
        { headerName: "Description", field: "description"},
    ]

    const [rowsData, setRowsData] = useState<TruliaListingSummary[]>([])
    const [fullRowsData, setFullRowsData] = useState<TruliaListingFull[]>([])
    
    useEffect(()=>{
        if (listings){
            let listingsList = returnTruliaFullAndSummaryListFromApiTruliaResponse(listings)
            setFullRowsData(listingsList.listingsFullList)
            setRowsData(listingsList.listingsSummaryList)
        }
    }, [listings])
    
    return (
        <Flex width="100%" height="100%" minHeight="250px" className="ag-theme-quartz">
            {   
                (listings !== undefined && !isFetching) 
                    ? <Box width="100%">
                        <AgGridReact
                            columnDefs={columnsData}
                            rowData={rowsData}
                            pagination={true}
                            paginationPageSize={500}
                            paginationPageSizeSelector={[100, 200, 500, 1000]}
                            onRowClicked={(e) => {onListingClick(e, fullRowsData)}}
                        />
                    </Box>
                    : <Box flex="1" alignSelf="center" justifySelf="center">
                        <Box as="i" className="fa fa-refresh fa-spin fa-10x"/>
                        <Text fontSize="3xl" marginTop="20px">Fetching all data... if page is not loaded in 30 seconds, please reload</Text>
                    </Box>       
            }
        </Flex>
        

    )
}
