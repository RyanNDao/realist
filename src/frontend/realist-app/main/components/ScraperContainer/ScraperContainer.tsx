import { Box, Button, Center, Flex } from "@chakra-ui/react";
import makeRequest from "../../helpers/apiHelper"
import React, { useEffect, useState } from "react";
import { useUser } from "../../hooks/useUser";

export function ScraperContainer() {
    const { user } = useUser();

    const [isFetching, setIsFetching] = useState(false);

    async function scrapeListings(){
        setIsFetching(true);
        try {
            await makeRequest('/api/trulia/scrape?searchType=FOR_SALE&limit=100', 'GET');
        } finally {
            setIsFetching(false)
        }
    }

    async function scrapeRentals(){
        setIsFetching(true);
        try {
            await makeRequest('/api/trulia/scrape?searchType=FOR_RENT&limit=100', 'GET');
        } finally {
            setIsFetching(false);
        }
    }

    async function scrapeSold(){
        setIsFetching(true);
        try {
            await makeRequest('/api/trulia/scrape?searchType=SOLD&limit=100&type=LAST_SALE_DATE', 'GET');
        } finally {
            setIsFetching(false);
        }
    }
    
    return (
        <Flex flexDirection="column" height="100%" justifyContent="space-between" gap="10px">
            <Center>
                <Button isDisabled={isFetching} onClick={scrapeListings}>Scrape Listings</Button>
                <Button isDisabled={isFetching} onClick={scrapeRentals}>Scrape Rentals</Button>
                <Button isDisabled={isFetching} onClick={scrapeSold}>Scrape Sold</Button>
            </Center>
        </Flex>
    )
}