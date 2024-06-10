import { Container, Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton, DrawerHeader, DrawerBody, Input, DrawerFooter, Button, Tabs, TabList, Tab, TabPanels, TabPanel } from "@chakra-ui/react";
import React, { useState } from "react";
import { RegistrationInputData, UserRegistrationForm } from "../../form_components/UserRegistrationForm"
import { LoginInputData, UserLoginForm } from "../../form_components/UserLoginForm";

type ProfileFormData = RegistrationInputData | LoginInputData;

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

    return (
        <Container>
            <Drawer
                isOpen={isOpen}
                placement='right'
                onClose={onClose}
            >
                <DrawerOverlay />
                <DrawerContent>
                    <DrawerCloseButton />
                    <Tabs onChange={(idx) => {handleTabChange(idx)}}>
                        <DrawerHeader>
                            <TabList>
                                <Tab>
                                    Register
                                </Tab>
                                <Tab>
                                    Login
                                </Tab>
                            </TabList>
                        </DrawerHeader>
    
                        <DrawerBody>
                            <TabPanels>
                                <TabPanel>
                                    <UserRegistrationForm 
                                        registrationInputData={profileFormData as RegistrationInputData} 
                                        updateData={setProfileFormData}
                                    />
                                    {JSON.stringify(profileFormData)}
                                </TabPanel>
                                <TabPanel>
                                    <UserLoginForm 
                                        loginInputData={profileFormData as LoginInputData} 
                                        updateData={setProfileFormData}
                                    />
                                    {JSON.stringify(profileFormData)}
                                </TabPanel>
                            </TabPanels>
                        </DrawerBody>
    
                        <DrawerFooter>
                            <Button variant='outline' mr={3} onClick={onClose}>
                                Cancel
                            </Button>
                            <Button colorScheme='blue'>{tabIndex === 0 ? 'Sign Up!' : 'Sign In!'}</Button>
                        </DrawerFooter>
                    </Tabs>
                </DrawerContent>
            </Drawer>
        </Container>
        
    )
}