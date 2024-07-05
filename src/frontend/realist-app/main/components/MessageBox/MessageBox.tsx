import React from "react";
import { Text } from "@chakra-ui/react";

interface MessageBoxProps {
    message: string;
    textColor?: string;
    success?: boolean;
    failure?: boolean
}


export function MessageBox ({message, textColor, success, failure}: MessageBoxProps){
    if (!textColor) {
        if (success) {
            textColor = 'green';
        } else if (failure) {
            textColor = 'red'
        } else {
            textColor = 'black'
        }
    }
    
    return (
        <Text color={textColor}>
            {message}
        </Text>
    )
}