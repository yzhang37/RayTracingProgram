# CS680 Lighting Shader Program

Student Name: **Zhenghang Yin**

Student ID: **U82871437**

***

## 1. Introduction

In this assignment, I used the OpenGL Shading Language (GLSL) to write my own vertex and fragment shaders to compute illumination and shading for meshes. I generated triangle meshes using the Element Buffer Object (EBO) and created displayable classes for an ellipsoid, torus, and cylinder with end caps. I also implemented normal rendering, illumination equations for diffuse, specular, and ambient light, and set up lights for point, infinite, and spotlight sources. In addition, I created multiple scenes featuring different objects and light configurations, and implemented texture and normal mapping as optional bonus tasks.

In addition to the basic functions, I have made several particularly beautiful and fancy scenes, as follows

*   **Scene 1: ** An earth globe with a normal map, a marble ring with a normal map, and a highlighted cone.

    ![](image/scene1.gif)

*   **Scene 2: **A scene similar to Phasmophobia, with a wooden floor (with a normal map), several flashlights, a basketball (with a normal map), an American football (with a normal map), and several ropes loops.

    ![](image/scene2.gif)

*   **Scene 3: **A beautiful Christmas table with lots of delicious donuts, cakes, and gift boxes. Using very rich lighting effects.

    ![](image/scene3.gif)

*   **Scene 4: **A pool table with a normal map, several balls, and a ball rack. There are also two lighting fixtures (one wireless light and one point light), and several spotlights.

    ![](image/scene4.gif)

## 2. How to use?

*   Press `1` through `9` to toggle the light switches in the scene (if the corresponding number exists)

*   Press `A` to turn on/off the ambient light

*   Press `S` to turn on/off the specular light

*   Press `D` to turn on/off the diffuse light

*   Use the left and right arrow keys to switch scenes

## 3. 完成的内容：

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
