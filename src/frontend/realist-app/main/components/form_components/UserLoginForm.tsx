import { Center, FormControl, FormLabel, VStack, Input, FormErrorMessage } from "@chakra-ui/react";
import React, { ChangeEvent, useState } from "react";

export interface LoginInputData {
    username: string,
    password: string
}

interface UserLoginFormProps {
    loginInputData: LoginInputData,
    updateData: (arg0: LoginInputData) => void
}
export function UserLoginForm({loginInputData, updateData}: UserLoginFormProps) {
    
    const onUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
        updateData({
            ...loginInputData,
            username: e.target.value
        })
    }

    const onPasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        updateData({
            ...loginInputData,
            password: e.target.value
        })
    }
    
    return (
        <VStack>
        <FormControl>
            <FormLabel>
                Username
            </FormLabel>
            <Input onChange={onUsernameChange} value={loginInputData.username} placeholder='JohnDoe123' />
        </FormControl>
        <FormControl isRequired={true} >
            <FormLabel>
                Password
            </FormLabel>
            <Input type="password" value={loginInputData.password} onChange={onPasswordChange} />
        </FormControl>
    </VStack>
    )
}