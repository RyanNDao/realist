import { Box, Flex, Heading, Spacer } from "@chakra-ui/react";
import React from "react";
import { AvatarWithSidebar } from "../AvatarWithSidebar/AvatarWithSidebar";

export function Header(){

    return (
        <Flex backgroundColor="lightgreen" padding="1rem 3rem">
            <Box>
                <Heading>Realist</Heading>
            </Box>
            <Spacer/>
            <AvatarWithSidebar/>
        </Flex>
    )
}