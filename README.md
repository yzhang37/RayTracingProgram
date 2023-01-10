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

## Model Design

本程序中使用了以下的模型：

1. 球体模型/椭球模型

   球体曲面参数方程，其中 $r$ 表示球体半径。
   $$
   \left \{
   \begin{aligned}
   x &= r \cdot \cos(\phi) \cdot \cos (\theta) \\
   y &= r \cdot \cos(\phi) \cdot \sin (\theta) \\
   z &= r \cdot \sin(\phi) \\
   \end{aligned}
   \right.,
   \phi \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right),
   \theta \in \left[-\pi, \pi\right),
   $$

   法线方程:
   $$
   \left \{
   \begin{aligned}
   nx &= \cos(\phi) \cdot \cos (\theta) \\
   ny &= \cos(\phi) \cdot \sin (\theta) \\
   nz &= \sin(\phi) \\
   \end{aligned}
   \right.,
   \phi \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right),
   \theta \in \left[-\pi, \pi\right),
   $$

   贴图位置：每个点 `[j/stacks, i/slices]`. 其中 `j/stacks` 表示 $\theta$ 的迭代,`i/slices`表示 $\phi$ 的迭代。具体定义见 [DisplayableSphere.py](DisplayableSphere.py).

   椭球模型和球体模型的参数非常相似，唯一的区别是将$r$换成了$a$, $b$, $c$，表示椭球三个不同的半径。具体定义见 [DisplayableEllipsoid.py](DisplayableEllipsoid.py).

3. 方体模型

   正方体模型一共8个点，面对不同的面有不同的法向量，均需要手动定义。具体 VBO/EBO 定义请参见[DisplayableCube.py](DisplayableCube.py), 此处不再赘述。

3. 圆柱体/圆锥体模型

   曲面参数方程:
   $$
   \newcommand{\low}{{r_{\mathrm{lower}}}}
   \newcommand{\upp}{{r_{\mathrm{upper}}}}
   \left \{
   \begin{aligned}
   x &= \left(\left(0.5 + \frac{u}{h}\right) · \low + \left(0.5 - \frac{u}{h}\right) · \upp \right) · \cos(\theta) \\
   y &= \left(\left(0.5 + \frac{u}{h}\right) · \low + \left(0.5 - \frac{u}{h}\right) · \upp \right) · \sin(\theta) \\
   z &= u \\
   u &\in \left[-\frac{h}{2}, \frac{h}{2}\right] \\
   \theta &\in \left[-\pi, \pi\right)
   \end{aligned}
   \right.
   $$
   其中, $r_{\mathrm{lower}}$ 表示圆锥体的下半径，$r_{\mathrm{upper}}$ 表示圆锥体的上半径。如果两个半径一致，则表现为一个圆柱体。$h$ 是高度。

   法线方程：

   - 在上表面是：$\vec{n}=[0, 0, 1]$

   - 在下表面是：$\vec{n}=[0, 0, -1]$

   - 在边上为：
     $$
     \newcommand{\csin}{{\mathbf{cSin}}}
     \vec{n}=[\cos(\theta) · \sqrt{1 - \csin^2}, \sin(\theta) · \sqrt{1 - \csin^2}, \csin]
     $$
     其中, $\mathbf{cSin} = (r_{\mathrm{lower}} - r_{\mathrm{upper}}) / h$.

   具体定义见 [DisplayableCylinder.py](DisplayableCylinder.py).

5. Torus 模型

   Torus 曲面参数方程:
   $$
   \left \{
   \begin{aligned}
   x &= (a + b \cdot \cos(\phi)) \cdot \cos (\theta) \\
   y &= (a + b \cdot \cos(\phi)) \cdot \sin (\theta) \\
   z &= b \cdot \sin(\phi) \\
   \end{aligned}
   \right.,
   \phi \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right),
   \theta \in \left[-\pi, \pi\right),
   $$
   
   其中 `a = (outer + inner) / 2`, `b = (outer - inner) / 2`.
   
   Torus 曲面法线方程:
   $$
   \left \{
   \begin{aligned}
   nx &= b · \cos(\theta) · \cos(\phi) · (a + b · \cos(\phi)) \\
   ny &= b · \sin(\theta) · \cos(\phi) · (a + b · \cos(\phi)) \\
   nz &= b · \sin(\phi) · (a + b · \cos(\phi)) \\
   \end{aligned}
   \right.,
   \phi \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right),
   \theta \in \left[-\pi, \pi\right),
   $$
   
   在标准化后为：
   $$
   \DeclareMathOperator{\sign}{sign}
   \DeclareMathOperator{\pat}{pat}
   \left \{
   \begin{aligned}
   \pat &= (a + b · \cos(\phi))\\
   nx &= \sign(b) · \cos(\theta) · \cos(\phi) · \sign(\pat) \\
   ny &= \sign(b) · \sin(\theta) · \cos(\phi) · \sign(\pat) \\
   nz &= \sign(b) · \sin(\phi) · \sign(\pat) \\
   \end{aligned}
   \right.,
   \phi \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right),
   \theta \in \left[-\pi, \pi\right),
   $$
   贴图位置：每个点 `[i/nsides, j / rings]`. 其中 `i/nsides` 表示 $\theta$ 的迭代,`j / rings`表示 $\phi$ 的迭代。具体定义见 [DisplayableTorus.py](DisplayableTorus.py).

## Features Included

| Requirements                                                           | Done |
| ---------------------------------------------------------------------- | ---- |
| Generate Triangle Meshes: Ellipsoid, Torus, and Cylinder with end caps | ✅    |
| Implement EBO for defining your meshes                                 | ✅    |
| Generate normals for your meshes, and implement normal visualization   | ✅    |
| Illuminate your meshes with diffuse, specular, and ambient components  | ✅    |
| Support 3 different light types (point, infinite, spotlight)           | ✅    |
| Create 3 different scenes                                              | ✅    |
| Texture mapping                                                        | ✅    |
| Normal mapping                                                         | ✅    |
| Artist Rendering                                                       |      |
