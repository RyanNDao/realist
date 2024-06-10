import { Button, Center } from "@chakra-ui/react";
import makeRequest from "../../helpers/apiHelper"
import React from "react";

export function ScraperContainer() {
    function scrapeWebsite(){
        makeRequest('/api/test-error', 'GET')
    }
    
    return (
        <Center>
            <Button onClick={scrapeWebsite}>Scrape</Button>
        </Center>
    )
}