import { Flex, Center, Button, Icon, Box, Select } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { TruliaListingsTable } from "../table_components/TruliaListingsTable/TruliaListingsTable";
import makeRequest from "../../helpers/apiHelper";
import { ApiTruliaListingResponse } from "../../helpers/globalInterfaces";
import { TruliaRentalsTable } from "../table_components/TruliaRentalsTable/TruliaRentalsTable";

export function DataContainer() {
    
    const [rentalData, setRentalData] = useState<ApiTruliaListingResponse[] | undefined>(undefined);
    const [listingsData, setListingsData] = useState<ApiTruliaListingResponse[] | undefined>(undefined);
    const [tableDataType, setTableDataType ] = useState<"listings" | "rentals" | "sold">("listings");
    const [isFetching, setIsFetching] = useState(false);

    async function getListingsFromDatabase(){
        return await makeRequest('api/trulia/get-listings', 'GET');
        
    }

    async function getRentalsFromDatabase(){
        return await makeRequest('api/trulia/get-rentals', 'GET');
    }

    const onSelectTableDataTypeChange = (event: any) => {
        const dataType = event.target.value;
        setTableDataType(dataType);
        console.log('Selected option:', dataType);
    }

    useEffect(()=>{
        async function fetchData() {
            console.log('Fetching data....')
            try {
                setIsFetching(true);
                const [listingsResponse, rentalResponse] = await Promise.all(
                    [
                        getListingsFromDatabase(), 
                        getRentalsFromDatabase()
                    ]
                )
                setListingsData(listingsResponse.data)
                setRentalData(rentalResponse.data)
            } catch {

            } finally {
                setIsFetching(false)
            }

            console.log('Rental/listings data has been fetched!')
        }
        console.log('Scraper container component built')
        fetchData();
    }, [])


    useEffect(() => {
        console.log('Updated listing and rental data:', listingsData, rentalData);
    }, [listingsData, rentalData]);
    
    return (
        <Flex flexDirection="column" height="100%" justifyContent="space-between" gap="10px">
            {!isFetching &&
                <Select width="60%" value={tableDataType} onChange={onSelectTableDataTypeChange}>
                    <option value='listings'>For Sale</option>
                    <option value='rentals'>For Rent</option>
                    <option value='sold'>Sold</option>
                </Select>
            }
            { tableDataType === "listings" &&
                <TruliaListingsTable
                    isFetching={isFetching}
                    listings={listingsData}
                />
            }
            { tableDataType === "rentals" &&
                <TruliaRentalsTable
                    isFetching={isFetching}
                    listings={rentalData}
                />
            }
            { tableDataType === "sold" &&
                <div>Coming soon</div>
            }
        </Flex>
    )
}