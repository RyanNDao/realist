import React from "react"
import { UserData } from "../../helpers/globalInterfaces"
import { Button, Center, DrawerFooter, DrawerHeader } from "@chakra-ui/react"
import { useUser } from "../../hooks/useUser";

interface ProfileInfoProps {
    user: UserData
}

export function ProfileInfo({user}: ProfileInfoProps) {
    const { logout } = useUser();
    
    return (
        <>
            <DrawerHeader>
                Hello {user.username}!
            </DrawerHeader>
            <DrawerFooter>
                <Button onClick={logout}>
                    Logout
                </Button>
            </DrawerFooter>
        </>
    )
}