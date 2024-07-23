import { Container, Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { RegistrationInputData, UserRegistrationForm } from "../form_components/UserRegistrationForm"
import { LoginInputData, UserLoginForm } from "../form_components/UserLoginForm";
import { ApiSuccessResponse } from "../../helpers/globalInterfaces";
import { useUser } from "../../hooks/useUser";
import { AuthenticationTabs } from "./AuthenticationTabs";
import { ProfileInfo } from "./ProfileInfo";

export type ProfileFormData = RegistrationInputData | LoginInputData;

interface SidebarProps {
    onClose: () => void,
    isOpen: boolean,
}

const emptyRegistrationData: RegistrationInputData = {
    username: '',
    password: '',
    confirmPassword: '',
}

const emptyLoginData: LoginInputData = {
    username: '',
    password: '',
}

export function ProfileSidebar({isOpen, onClose}: SidebarProps){

    const [profileFormData, setProfileFormData] = useState<ProfileFormData>(emptyRegistrationData);
    const [tabIndex, setTabIndex] = useState<number>(0);
    const [message, setMessage] = useState('');
    const [success, setSuccess] = useState(false);
    const [failure, setFailure] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const { login, user } = useUser();


    const handleTabChange = (idx: number) => {
        if (idx == 0) { // on registration tab
            setProfileFormData(emptyRegistrationData);
        } else if (idx == 1) { // on login tab
            setProfileFormData(emptyLoginData);
        } else {
            // add more tabs here if needed
        }
        setTabIndex(idx);
    } 

    const onUserFormButtonClick = async () => {
        if (tabIndex == 0) { // on registration tab
            
        } else if (tabIndex == 1) { // on login tab
            try {
                setIsLoading(true);
                let data: ApiSuccessResponse = await login(profileFormData.username, profileFormData.password)
                setMessage(data.message);
                setFailure(false);
                setSuccess(true);
            } catch (error) {
                setMessage(error.toString());
                setFailure(true);
                setSuccess(false);
            } finally {
                setIsLoading(false)
            }
        } else {
            // add more tabs here if needed
        }
    }

    return (
        <Container>
            <Drawer
                isOpen={isOpen}
                placement='right'
                onClose={onClose}
            >
                <DrawerOverlay />
                <DrawerContent>
                    <DrawerCloseButton zIndex={1}/>
                    { user 
                        ?
                        <ProfileInfo
                            user={user}
                        />
                        :
                        <AuthenticationTabs 
                            onChange={(idx)=>{handleTabChange(idx)}}
                            onUserFormButtonClick={onUserFormButtonClick}
                            onClose={onClose}
                            tabIndex={tabIndex}
                            profileFormData={profileFormData}
                            setProfileFormData={setProfileFormData}
                            message={message}
                            success={success}
                            failure={failure}
                            isLoading={isLoading}
                        />
                    }
                </DrawerContent>
            </Drawer>
        </Container>
        
    )
}