# Tetris

A classic Tetris game built with Python and Pygame.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tetris.git
   cd tetris
   ```

2. Install Pygame:
   ```bash
   pip install pygame
   ```

## Usage

Run the game:
```bash
python Tetris.py
```

## Controls

| Key | Action |
|-----|--------|
| Left Arrow | Move piece left |
| Right Arrow | Move piece right |
| Down Arrow | Soft drop (faster fall) |
| Up Arrow | Rotate piece |
| Space | Hard drop (instant drop) |
| Escape | Pause game |

## Scoring

- **Soft drop**: 1 point per row
- **Hard drop**: 2 points per row
- **Line clears** (multiplied by level):
  - 1 line: 40 points
  - 2 lines: 100 points
  - 3 lines: 300 points
  - 4 lines (Tetris): 1200 points

## Level Progression

- Clear 10 lines to advance to the next level
- Each level increases the fall speed

## License

This project is open source and available under the MIT License.
