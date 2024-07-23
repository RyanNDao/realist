import { Box, Flex, Text, VStack } from "@chakra-ui/react";
import React from "react";
import { TruliaListingFull, TruliaListingModalAdditionalInfo, TruliaListingModalOverview } from "../../helpers/globalInterfaces";
import { ListingDataContent } from "./ListingDataContent";
import { ModalViewState } from "./TruliaDataModal";
import { ListingDescriptionContent } from "./ListingDescriptionContent";
import { ListingPriceHistoryContent } from "./ListingPriceHistoryContent";
import { formatNumberToMoney } from "../../helpers/common";

interface TruliaDataModalBodyProps{
    activeListing: TruliaListingFull;
    modalView: ModalViewState;
}

export function TruliaDataModalBody({activeListing, modalView}: TruliaDataModalBodyProps) {
    
    const overviewData: TruliaListingModalOverview = {
        askingPrice: formatNumberToMoney(activeListing.askingPrice),
        bedrooms: activeListing.bedrooms,
        bathrooms: activeListing.bathrooms,
        neighborhood: activeListing.neighborhood,
        floorSqft: activeListing.floorSqft,
        lotSqft: activeListing.lotSqft,
        propertyType: activeListing.propertyType,
        propertySubType: activeListing.propertySubType,
        yearBuilt: activeListing.yearBuilt,
        yearRenovated: activeListing.yearRenovated,
        condition: activeListing.condition,
    }

    const additionalData: TruliaListingModalAdditionalInfo = {
        architecture: activeListing.architecture,
        basement: activeListing.basement,
        foundation: activeListing.foundation,
        houseMaterial: activeListing.houseMaterial,
        structureType: activeListing.structureType,
        parking: activeListing.parking,
        dateListedOrSold: activeListing.dateListedOrSold,

    }
    
    
    return (
        <Flex flexDirection="column">
            {modalView === "overview" &&
                <Flex direction="column" gap="10px">
                    <ListingDataContent heading="Overview" data={overviewData}/>
                    <ListingDataContent heading="Additional Data" data={additionalData}/>
                </Flex>
            }
            {modalView === "description" &&
                ( activeListing.description 
                    ? <ListingDescriptionContent description={activeListing.description}/>
                    : <Text>No Description Found</Text>
                )
            }
            {modalView === "history" &&
                ( activeListing.priceHistory?.length
                    ? <ListingPriceHistoryContent priceHistory={activeListing.priceHistory}/>
                    : <Text>No Price History Found</Text>
                )
            }
        </Flex>
    )
}