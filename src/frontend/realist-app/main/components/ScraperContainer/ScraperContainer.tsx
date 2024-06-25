import { Button, Center } from "@chakra-ui/react";
import makeRequest from "../../helpers/apiHelper"
import React from "react";

export function ScraperContainer() {
    function scrapeWebsite(){
        makeRequest('/api/trulia/scrape/for_sale', 'GET')
    }

    function scrapeRentals(){
        makeRequest('/api/trulia/scrape/for_rent', 'GET')
    }
    
    return (
        <Center>
            <Button onClick={scrapeWebsite}>Scrape Listings</Button>
            <Button onClick={scrapeRentals}>Scrape Rentals</Button>
        </Center>
    )
}