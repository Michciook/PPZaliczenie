# Realm of the *** ***

## Project Description
"Realm of the *** ***" is a 2D top-down shooter game built using Python and the Pygame library. Players can choose between two character classes, Wizard and Knight, each with unique abilities. The game features an endless battle against enemy waves, where players must strategically move, shoot, and use their abilities to survive as long as possible.

## Features
- **Character Selection**: Choose between a **Wizard** or a **Knight**, each with different abilities and stats.
- **Combat System**: Players can shoot projectiles at enemies and use special abilities.
- **Enemy AI**: Enemies hunt down the player and shoot projectiles.
- **Health & Mana System**: Players have health and mana bars, with mana regenerating over time.
- **Camera System**: The camera follows the player's movement, providing a dynamic view.
- **Main Menu & Class Selection**: Navigate through the game with a menu system.

## Installation
To run the game, ensure you have Python installed on your system along with the required dependencies.

### Prerequisites
- Python 3.x
- Pygame

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Michciook/PPZaliczenie.git
   ```
2. Navigate to the project folder:
   ```sh
   cd PPZaliczenie
   ```
3. Install the required dependencies:
   ```sh
   pip install pygame
   ```
4. Run the game:
   ```sh
   python main.py
   ```

## Controls
- **W, A, S, D**: Move the player
- **Left Mouse Button**: Shoot projectiles
- **Spacebar**: Use special ability

## Game Mechanics
- **Wizard's Ability**: Shoots projectiles in a circular pattern.
- **Knight's Ability**: Shoots three projectiles in a spread pattern.
- **Enemies**: Chase and shoot at the player. The game spawns additional enemies over time.
- **Health and Mana**:
  - Taking damage decreases health.
  - Using abilities consumes mana, which regenerates gradually.

## Files & Structure
- `main.py`: The main game file that runs the game loop.
- `settings.py`: Contains game constants such as screen size, player speed, and cooldowns.
- `Background.png`, `Player.png`, `PlayerKnight.png`, `Bullet.png`, `enemy.png`: Game assets.

## Credits
This game was developed as a university project using **Python** and **Pygame**.

## License
This project is for educational purposes and is not intended for commercial use. Feel free to modify and expand upon it!

