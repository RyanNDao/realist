import React from "react";
import { TruliaListingFull, TruliaListingModalAdditionalInfo, TruliaListingModalOverview } from "../../helpers/globalInterfaces";
import { Box, Flex, Heading } from "@chakra-ui/react";
import { KeyValueTextField } from "../KeyValueTextField/KeyValueTextField";
import { formatCamelCase } from "../../helpers/common";

interface ListingDataContentProps{
    heading: string;
    data: TruliaListingModalOverview | TruliaListingModalAdditionalInfo;
}

export function ListingDataContent({heading, data}: ListingDataContentProps){
    
    return (
        <Flex flexDirection="column">
            <Heading textDecoration="underline" size="md">{heading}</Heading>
            {Object.entries(data).map((keyValuePairArray) => {
                if (keyValuePairArray[1]) {
                    return <KeyValueTextField 
                        keyName={formatCamelCase(keyValuePairArray[0])} 
                        value={keyValuePairArray[1]}
                        key={keyValuePairArray[0]}
                    />
                }
            })}
        </Flex>
    )
}