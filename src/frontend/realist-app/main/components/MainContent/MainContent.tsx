import { Flex, TabPanel, TabPanels } from "@chakra-ui/react";
import React from "react";
import { ScraperContainer } from "../ScraperContainer/ScraperContainer";

export function MainContent({tabIndex}) {

    return (
        <Flex>
            <TabPanels>
                <TabPanel>kk</TabPanel>
                <TabPanel>
                    <ScraperContainer></ScraperContainer>
                </TabPanel>
            </TabPanels>
        </Flex>
    )
}