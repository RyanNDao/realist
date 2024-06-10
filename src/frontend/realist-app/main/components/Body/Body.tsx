import { Box, Flex, Tabs } from "@chakra-ui/react";
import React, { useState } from "react";
import { Sidebar } from "../Sidebar/Sidebar";
import { MainContent } from "../MainContent/MainContent";

interface BodyProps {
    
}

export function Body(){
    const [tabIndex, setTabIndex] = useState<number>(0)
    const switchTabs = (index: number) => {
        setTabIndex(index);
    };


    return (
            <Tabs flexGrow={1} isFitted variant="enclosed" orientation="vertical">
                
                    <Sidebar tabIndex={tabIndex}/>
                    <MainContent tabIndex={tabIndex}/>
                
            </Tabs>


      );
}