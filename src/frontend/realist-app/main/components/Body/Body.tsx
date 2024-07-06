import { Box, Flex, Tabs, useBreakpointValue } from "@chakra-ui/react";
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
    const responseOrientation = useBreakpointValue<'vertical' | 'horizontal' | undefined>(
        { base: 'horizontal', md: 'vertical' }
    );

    return (
        <Tabs flexGrow={1} isFitted variant="enclosed" orientation={responseOrientation}>
            <Sidebar tabIndex={tabIndex}/>
            <MainContent tabIndex={tabIndex}/>
        </Tabs>
      );
}