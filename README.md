# Tic-Tac-Fade
#### Video Demo:  <TODO>
## 📝 Description:

&emsp;We all know and love **Tic-Tac-Toe** however we also know it's flaw - it can be repetitive and unfair, especially when first player (X typically first move) knows a perfect strategy to win everytime. 

&emsp;In this project, I present a twist on Tic-Tac-Toe, a concept inspired of **Tic-Tac-Bolt**, and I named it **`Tic-Tac-Fade`**. A variation where players can only have three active moves at the board. When the fourth move is next the oldest move will fade it's opacity, then after deciding on a move faded move will disappear. By doing this we can keep the game dynamic and strategic.

## 🎮 Game mechanics description:
- Classic 3×3 Tic Tac Toe with a slight variation.
- But instead of just marking and ending when someone gets 3, each player can only have 3 active moves on the board at any time.
- When a player places a 4th move, their oldest move fades away, and the square becomes free again.
- The same rule applies to both X and O.
- You can’t place a new move on your own faded square again until it’s free.

This approach prevents stale, repetitive strategies and keeps the gameplay fresh.

## 🛠️ Why Pygame?
&emsp;The project primarily use the library of **`pygame-ce`**, it is same as pygame but a more maintained version of it. Moreover before choosing the pygame there's another option which is **`tk`**. Since I'm familiar with java swing, tk would be easier to work with, however since it's nice learn new things, I chose pygame.

## 🗃️ File and Class Overview
- **`project.py`** - The main entry point of the program. It manages the overall game state, event loop, and user interface rendering.
- **`panel.py`** - A layout and panel management module inspired by Java Swing-style placement. It handles responsive positioning and sizing of UI elements.
- **`play_area.py`** - Contains the logic for the game board and player interactions. It manages the 3x3 grid, move placement, win checking, and the fading mechanic that limits each player to 3 active moves.
- **`my_color.py`** - Color definitions for the game. This file stores and manages all color values used to maintain a consistent and visually appealing design.
- **`test_project.py`** - Testing custom function logic from the main project code.

## ▶️ How to Run the Project
### 1. Install Visual Studio Code  
Download from: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2. Install Python 3  
Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
Check installation by running:

```bash
python --version
```
Make sure to check “Add Python to PATH” during installation on Windows.

### 3. Clone or Download the Project

    git clone https://github.com/your-username/tic-tac-fade.git
    cd tic-tac-fade

Or manually download and extract the ZIP.

### 4. (Optional) Create a Virtual Environment

    python -m venv venv

Then activate:

    venv\Scripts\activate     # On Windows
    source venv/bin/activate  # On macOS/Linux

### 5. Install Requirements

    pip install -r requirements.txt

### 6. Run the Game

    python project.py

The game window should appear, and you can start playing Tic-Tac-Fade!

#### Let me know your experience and opinion to improve the game
email: josephcanzana04@gmail.com