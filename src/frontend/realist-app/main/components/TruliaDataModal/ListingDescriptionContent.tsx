import React from "react";
import { Flex, Text, Heading } from "@chakra-ui/react";

interface ListingDescriptionContentProps{
    description: string
}

export function ListingDescriptionContent({description}: ListingDescriptionContentProps){
    
    return (
        <Flex flexDirection="column">
            <Heading textDecoration="underline" size="md">Listing Description</Heading>
            <Text>{description}</Text>
        </Flex>
    )
}