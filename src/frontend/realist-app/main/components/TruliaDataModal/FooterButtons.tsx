import { Button, Flex } from "@chakra-ui/react";
import React, { ReactElement } from "react";
import { ModalViewState } from "./TruliaDataModal";

interface FooterButtonsProps{
    setModalView: (arg0: ModalViewState) => void;
}

export function FooterButtons({setModalView}: FooterButtonsProps){
    return (
        <Flex gap="7px">
            <Button onClick={()=>{setModalView("overview")}}>Overview</Button>
            <Button onClick={()=>{setModalView("description")}}>Description</Button>
            <Button onClick={()=>{setModalView("history")}}>History</Button>
        </Flex>
    )
}