import { VStack, Box } from "@chakra-ui/react";
import React, { ChangeEvent, useState } from "react";

export interface RegistrationInputData {
    username: string,
    password: string,
    confirmPassword: string
}

interface UserRegistrationFormProps {
    registrationInputData: RegistrationInputData,
    updateData: (arg0: RegistrationInputData) => void
}

export function UserRegistrationForm ({registrationInputData, updateData}: UserRegistrationFormProps) {
    const doPasswordsMatch = registrationInputData.password === registrationInputData.confirmPassword;
    
    const onUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
        updateData({
            ...registrationInputData,
            username: e.target.value
        })
    }

    const onPasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        updateData({
            ...registrationInputData,
            password: e.target.value
        })
    }

    const onConfirmPasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        updateData({
            ...registrationInputData,
            confirmPassword: e.target.value
        })
    }

    return (
        <VStack>
            <div>Coming Soon!</div>
            <Box textAlign="center">For now, get your login information from Ryan</Box>
            {/* <FormControl>
                <FormLabel>
                    Username
                </FormLabel>
                <Input onChange={onUsernameChange} value={registrationInputData.username} placeholder='JohnDoe123' />
            </FormControl>
            <FormControl isRequired={true} >
                <FormLabel>
                    Password
                </FormLabel>
                <Input type="password" value={registrationInputData.password} onChange={onPasswordChange} />
            </FormControl>
            <FormControl isRequired={true} isInvalid={!doPasswordsMatch}>
                <FormLabel>
                    Confirm Password
                </FormLabel>
                <Input type="password" value={registrationInputData.confirmPassword} onChange={onConfirmPasswordChange} />
                <FormErrorMessage>Passwords must match!</FormErrorMessage>
            </FormControl> */}
        </VStack>
    )
}