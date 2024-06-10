import { Flex, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import React from "react";

interface SidebarProps {
    tabIndex: number
}

export function Sidebar({tabIndex}: SidebarProps){
    return (
        <Flex p="5px" direction="column">
            <TabList flexGrow={1}>
                <Tab>Home</Tab>
                <Tab>Scraper</Tab>
            </TabList>
        </Flex>
    )
}