import { Button, Box, useDisclosure, Avatar } from "@chakra-ui/react";
import React from "react";
import { ProfileSidebar } from "../ProfileSidebar/ProfileSidebar";

export function AvatarWithSidebar(){
    const { isOpen, onOpen, onClose } = useDisclosure()

    return(
        <Box>
            <Avatar cursor="pointer" onClick={onOpen}/>
            {isOpen && <ProfileSidebar isOpen={isOpen} onClose={onClose}/>}
        </Box>

    )
}