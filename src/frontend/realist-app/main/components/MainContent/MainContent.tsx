import { Box, Flex, TabPanel, TabPanels, Text, useBreakpointValue } from "@chakra-ui/react";
import React from "react";
import { ScraperContainer } from "../ScraperContainer/ScraperContainer";
import { useUser } from "../../hooks/useUser";
import { DataContainer } from "../DataContainer/DataContainer";

export function MainContent({tabIndex}) {
    const { user } = useUser();
    const responsivePaddingBottom = useBreakpointValue(
        { base: '15%', md: '5%' }
    );
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
                        <DataContainer/>
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