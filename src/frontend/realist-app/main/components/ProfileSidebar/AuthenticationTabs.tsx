import { Button, DrawerBody, DrawerFooter, DrawerHeader, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react"
import React from "react"
import { UserLoginForm, LoginInputData } from "../form_components/UserLoginForm"
import { UserRegistrationForm, RegistrationInputData } from "../form_components/UserRegistrationForm"
import { MessageBox } from "../MessageBox/MessageBox"
import { ProfileFormData } from "./ProfileSidebar"

interface AuthenticationTabsProps {
    onChange: (arg0: number) => void;
    onUserFormButtonClick: () => Promise<void>;
    onClose: () => void;
    tabIndex: number;
    profileFormData: ProfileFormData;
    setProfileFormData: React.Dispatch<React.SetStateAction<ProfileFormData>>;
    message?: string;
    success?: boolean;
    failure?: boolean;
    isLoading?: boolean
}

export function AuthenticationTabs ({onChange, onUserFormButtonClick, onClose, tabIndex, profileFormData, setProfileFormData, message, success, failure, isLoading}: AuthenticationTabsProps) {
    return (
        <Tabs onChange={onChange}>
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
                    </TabPanel>
                    <TabPanel>
                        <UserLoginForm 
                            loginInputData={profileFormData as LoginInputData} 
                            updateData={setProfileFormData}
                        />
                        {JSON.stringify(profileFormData)}
                        {message && <MessageBox message={message} success={success} failure={failure}></MessageBox>}
                    </TabPanel>
                </TabPanels>
            </DrawerBody>

            <DrawerFooter justifyContent="center">
                <Button variant='outline' mr={3} onClick={onClose}>
                    Cancel
                </Button>
                <Button onClick={onUserFormButtonClick} isDisabled={tabIndex === 0 || isLoading} colorScheme='blue'>
                    {tabIndex === 0 ? 'Sign Up!' : 'Sign In!'}
                </Button>
            </DrawerFooter>
        </Tabs>
    )
}