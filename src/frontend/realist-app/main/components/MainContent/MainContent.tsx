import { Box, Flex, TabPanel, TabPanels, Text, useBreakpointValue } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { ScraperContainer } from "../ScraperContainer/ScraperContainer";
import { useUser } from "../../hooks/useUser";
import { DataContainer } from "../DataContainer/DataContainer";
import { ApiTruliaListingResponse } from "../../helpers/globalInterfaces";
import makeRequest from "../../helpers/apiHelper";

export function MainContent({tabIndex}) {
    const { user } = useUser();
    const responsivePaddingBottom = useBreakpointValue(
        { base: '15%', md: '5%' }, { ssr: false }
    );
    const [rentalData, setRentalData] = useState<ApiTruliaListingResponse[] | undefined>(undefined);
    const [listingsData, setListingsData] = useState<ApiTruliaListingResponse[] | undefined>(undefined);
    const [soldData, setSoldData] = useState<ApiTruliaListingResponse[] | undefined>(undefined);
    
    const [isFetching, setIsFetching] = useState(false);

    async function getListingsFromDatabase(){
        return await makeRequest('api/trulia/get-listings', 'GET');
        
    }

    async function getRentalsFromDatabase(){
        return await makeRequest('api/trulia/get-rentals', 'GET');
    }

    async function getSoldPropertiesFromDatabase(){
        return await makeRequest('api/trulia/get-sold', 'GET');
    }

    useEffect(()=>{
        async function fetchData() {
            console.log('Fetching data....')
            try {
                setIsFetching(true);
                const [listingsResponse, rentalResponse, soldResponse] = await Promise.all(
                    [
                        getListingsFromDatabase(), 
                        getRentalsFromDatabase(),
                        getSoldPropertiesFromDatabase()
                    ]
                )
                setListingsData(listingsResponse.data)
                setRentalData(rentalResponse.data)
                setSoldData(soldResponse.data)
            } catch {

            } finally {
                setIsFetching(false)
            }

            console.log('Rental/listings/sold data has been fetched!')
        }
        console.log('Scraper container component built')
        if (user){
            fetchData();

        }
    }, [user])


    useEffect(() => {
        console.log('Updated listing and rental data:', listingsData, rentalData);
    }, [listingsData, rentalData]);

    return (
        <Flex width="100%" height="100%">
            <TabPanels>
                <TabPanel height="100%" paddingBottom={responsivePaddingBottom}>
                    <Box>
                        Welcome to Realist, more features coming soon!
                        {!user &&
                        <Text>
                            Log in to get more access to Realist!
                        </Text>
                        }
                    </Box>
                
                </TabPanel>
                {user &&
                    <TabPanel height="100%" paddingBottom={responsivePaddingBottom}>
                        <DataContainer
                            isFetching={isFetching}
                            rentalData={rentalData}
                            listingsData={listingsData}
                            soldData={soldData}
                        />
                    </TabPanel>
                }
                {user?.isAdmin &&
                    <TabPanel height="100%" paddingBottom={responsivePaddingBottom}>
                        <ScraperContainer/>
                    </TabPanel>
                }
            </TabPanels>
        </Flex>
    )
}