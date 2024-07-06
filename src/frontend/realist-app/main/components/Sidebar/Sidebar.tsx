import { Flex, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import React from "react";
import { useUser } from "../../hooks/useUser";

interface SidebarProps {
    tabIndex: number
}

export function Sidebar({tabIndex}: SidebarProps){
    const { user } = useUser();
    
    return (
        <Flex p="5px" direction="column">
            <TabList flexGrow={1}>
                <Tab>Home</Tab>
                {user && <Tab>Data</Tab>}
                {user?.isAdmin && <Tab>Scraper</Tab>}
            </TabList>
        </Flex>
    )
}