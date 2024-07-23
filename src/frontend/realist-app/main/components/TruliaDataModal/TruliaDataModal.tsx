import { Button, Text, Box, Link, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure, Flex, useBreakpointValue } from "@chakra-ui/react";
import React, { ReactElement, useCallback, useEffect, useState } from "react";
import { TruliaListingFull } from "../../helpers/globalInterfaces";
import { TruliaDataModalBody } from "./TruliaDataModalBody";
import { FooterButtons } from "./FooterButtons";


interface TruliaDataModalProps {
    isOpen: boolean;
    setIsOpen: (arg0: boolean) => void;
    activeListing: TruliaListingFull
}

export type ModalViewState = "overview" | "description" | "history"


export function TruliaDataModal({isOpen, setIsOpen, activeListing}: TruliaDataModalProps) {
    
    const { onClose } = useDisclosure({ defaultIsOpen: true })

    const [modalView, setModalView] = useState<ModalViewState>("overview")
    
    const closeModal = () => {
        setIsOpen(false)
        onClose()
    }


    useEffect(()=> {
        setModalView("overview");
    }, [isOpen])

    const responsiveFooterAlignment = useBreakpointValue<any>(
        { base: 'column', md: 'row' }, { ssr: false }
    );

    return (
        <>
            <Modal 
                isOpen={isOpen} 
                onClose={closeModal} 
                size="xl"
                scrollBehavior="inside"
            >
            <ModalOverlay />
            <ModalContent>
                <ModalHeader fontSize="2xl">
                    { activeListing.trulia_url 
                        ? <Link href={`https://${activeListing.trulia_url}`} isExternal>
                            {activeListing.key} <Box as="i" className="fa fa-external-link fa-2xs"></Box>
                        </Link>
                        : <>{activeListing.key}</>
                    }

                </ModalHeader>
                <ModalCloseButton />
                
                <ModalBody>
                    <TruliaDataModalBody
                        activeListing={activeListing}
                        modalView={modalView}
                    />
                </ModalBody>

                <ModalFooter>
                    <Flex gap="10px" flexDirection={responsiveFooterAlignment} flex="1" justifyContent="space-between">
                        <FooterButtons setModalView={setModalView}/>
                        <Text alignSelf="center" color="grey">{`Last Updated: ${activeListing.dateScraped}`}</Text>
                    </Flex>
                </ModalFooter>
            </ModalContent>
        </Modal>
        </>
    )
}