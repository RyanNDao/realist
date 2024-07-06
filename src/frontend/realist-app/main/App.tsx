import { useState } from 'react'
import './App.css'
import { Box, Button, Container, Drawer, DrawerBody, DrawerCloseButton, DrawerContent, DrawerFooter, DrawerHeader, DrawerOverlay, Flex, Image, Input, useDisclosure } from '@chakra-ui/react'
import React from 'react'
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'
import { Header } from './components/Header/Header'
import { Body } from './components/Body/Body'

function App() {

  return (
    <Flex direction="column" maxHeight="100vh" maxWidth="100vw" height="100%" width="100%">
        <Header/>
        <Body/>
    </Flex>
  )
}

export default App
