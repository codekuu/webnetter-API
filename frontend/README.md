<p align="center">
  <img src="https://i.imgur.com/SWoPeSe.png">
Frontend/ GUI for Webnetter API (Plug and Play Network Management API built on top of Netmiko)
</p>

## Quick Links:
- [Description](#description)
- [Setup](#setup)
- [Contribute](contribute)

[:computer: Click here for Live demo :computer:](https://oppetinternet.se/webnetter)


## Description

The goal of the Webnetter API is to make it a portable but also a static Network Management tool for any network.
Frontend/ GUI is optional in Webnetter API and built on Vue with Vuetify.

This REPO is the frontend/GUI for Webnetter API.
You can find Webnetter API [HERE](https://github.com/codekuu/webnetter-API).

Directories:
```
-- src
    -- api
    -- components
    |   -- Common
    |   -- Layout
    |       -- AppHeader
    |       -- AppSidebar
    -- plugins
    -- routes
    |   -- Overview
    |   -- Webnetter
    |       -- configure
    |       -- runCommands
    |       -- scp
    -- vuex

```

## Setup

    npm install

**Start locally** (Standard: localhost:8080)

    npm run serve

**Build final dist folder**

    npm run build
 
If you would like to copy your changes over to the Webnetter API you can just remove the app/dist folder and replace it with the new dist that got built.

## Contribute

**Do you have ideas?**
We are open for future development ideas, start an issue and tell us what you would like to have implemented.

**Found an error or want to help me write better code?**
We love critic, if you find something in the code that's bad or can be enhached please start an issue and we will respond you as fast as I can.

# We :dog: OPEN SOURCE
