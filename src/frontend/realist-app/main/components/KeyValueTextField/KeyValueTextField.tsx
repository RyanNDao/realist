import { Box, Flex, Text } from "@chakra-ui/react";
import React from "react";

interface KeyValueTextFieldProps {
    keyName: string;
    value: any;
    color?: string;
}

export function KeyValueTextField({keyName, value, color}: KeyValueTextFieldProps) {
    return (
        <Box>
            <Text fontWeight="bold" display="inline">{keyName}</Text>
            <Text display="inline">: {value}</Text>
        </Box>
    )
}