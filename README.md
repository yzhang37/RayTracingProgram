# Lighting Shader Program with PyOpenGL

## Introduction

To begin, I utilized five different surface shapes such as spheres, ellipsoids, rectangles, cones (cylinders), and torus (donut shapes). I wrote my own code for creating the surface mesh and defining the vertex buffer and index buffer. I then implemented various rendering techniques, including basic rendering, diffuse reflection, specular reflection, ambient lighting, texture mapping, and normal mapping. I also distinguished between point lighting, directional lighting, and spotlight effects. Ultimately, I produced several stunning scenes.

The following are the four scenarios of this program:

![Scene Introduction](image/scene_intro.gif)

## Usage

| Keys                      | Functions                                                    |
| ------------------------- | ------------------------------------------------------------ |
| Numeric keys (`1` to `9`) | Toggle the light switches in the scene (if the corresponding number exists) |
| `A`                       | Turn on/off the ambient rendering mode.                      |
| `S`                       | Turn on/off the specular rendering mode.                     |
| `D`                       | Turn on/off the diffuse rendering mode.                      |
| `←` / `→`                 | Switch scenes.                                               |

## Scene design

*   **Scene 1:** This scene is a testing scene, primarily used to ensure that the VBO/EBO implementation of this program is functioning correctly. It includes an 🌏 earth (sphere shape), a ring ashtray (torus shape), and a half cone, all with metallic surface applied. There are also three point lights present in the scene, colored blue, red, and yellow, that are flying around.

    https://user-images.githubusercontent.com/17313035/211599858-4d0741f7-3ceb-4bdd-bab9-2c8b53d556cd.mp4

*   **Scene 2:** The second scene is similar to the high school map in the game [Phasmophobia](https://web.archive.org/web/20230109084122/https://kineticgames.co.uk/). It features a wooden floor of a basketball court, on which there is a 🏀basketball (sphere model), an 🏈 American football (ellipsoid model), several rings (randomly colored red or blue, torus model for the ring, cylinder model for the stick). In order to create a horror-like atmosphere, I intentionally made the environment dark and added several 🔦 flashlights, to create a atmosphere of dimness.

    https://user-images.githubusercontent.com/17313035/211599902-72e0fd42-580d-4fa1-babd-d02e1e113610.mp4

*   **Scene 3:** The third scene is a beautifully set dining table with a plethora of donuts 🥯 (All come in Glazed flavor, which is my favorite flavor. You might gain 10lbs if you ate them all 😂lol), several nicely decorated 🎁 Christmas gift boxes, chocolate cakes and elegant candles. The surface of the Christmas gift box has a reflective mirror-like effect (resembling tin foil). The donuts are textured using a special normal map that makes them look incredibly realistic! (The specific texture file can be found in the /assets folder). The only downside is that I didn't implement a shadow effect, so the candle light will shine through the cakes and it will give the impression of a very bright light beneath the cakes.

    https://user-images.githubusercontent.com/17313035/211606642-e3cca8b8-35ef-41da-b7c1-6c181b02040a.mp4

*   **Scene 4:** This is a finely crafted scene featuring a 🎱 pool table with a smooth, comfortable texture and an orderly pattern of stripes. A series of pool balls and a rack are placed on the table. Four flashlight beams illuminate the center of the table and two fluorescent lamps are used for lighting. In this scene, I used a normal map to achieve the feel of the fabric on the pool table. The fluorescent lamps use an infinite light and the flashlight beams use a spotlight effect.

    https://user-images.githubusercontent.com/17313035/211105179-6839973b-d054-4b16-8123-666d354238b8.mp4

## Features Included

| Requirements                                                           | Done |
| ---------------------------------------------------------------------- | ---- |
| Generate Triangle Meshes: Ellipsoid, Torus, and Cylinder with end caps | √    |
| Implement EBO for defining your meshes                                 | √    |
| Generate normals for your meshes, and implement normal visualization   | √    |
| Illuminate your meshes with diffuse, specular, and ambient components  | √    |
| Support 3 different light types (point, infinite, spotlight)           | √    |
| Create 3 different scenes                                              | √    |
| Texture mapping                                                        | √    |
| Normal mapping                                                         | √    |
| Artist Rendering                                                       |      |
