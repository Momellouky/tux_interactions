# SuperTuxKart Interaction Techniques Project

## Overview

Welcome to the SuperTuxKart Interaction Techniques Project! This project focuses on developing and implementing new interaction techniques for enhancing the gameplay experience in SuperTuxKart, an open-source kart racing game.

## Project Goals

- **Innovation:** Introduce novel interaction techniques that add excitement and engagement to the gameplay.
- **User Experience:** Enhance the overall user experience by improving controls, responsiveness, and accessibility.
- **Compatibility:** Ensure compatibility with various platforms and input devices.

## Features

- **New Controls:** Introduce alternative control schemes or enhance existing ones for a more immersive experience.
- **Multiplayer Interaction:** Implement features that enhance interaction between players in multiplayer mode.
- **Accessibility Features:** Develop features to improve the accessibility of the game for a broader audience.
- **Customization:** Allow players to customize their interaction preferences and key bindings.

## Getting Started

### Requirements

The Arduino sketch uses the Grove Ultrasonic Ranger sensor, which needs the [UltrasonicRanger library](https://github.com/Seeed-Studio/Seeed_Arduino_UltrasonicRanger/archive/master.zip) (link to zip) to be downloaded from GitHub and installed.

### Execution

- First, set up your Arduino : Grove Base Shield, Grove Ultrasonic Ranger sensor plugged onto D7, Grove Tilt Switch plugged onto D5.
- Upload ArduinoToSerial sketch to your Arduino.
- Launch MCSI_serveur Python script in a terminal. You should see "STK input server started" in the terminal.
- Open SuperTuxKart and navigate to a track.
    - It's recommended to do this before launching MCSI_client Python script because the client manipulates keyboard inputs, which can lead to unwanted behavior outside of a race track.
- Launch MCSI_client, arduino_client and mic_client in terminals. Each of them waits for 5 seconds before sending any inputs.
- You can start playing !