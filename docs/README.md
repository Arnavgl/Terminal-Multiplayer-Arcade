````markdown
# 🎮 Terminal Multiplayer Arcade

A sophisticated Python-based multiplayer game server that brings classic arcade games to the terminal with real-time networking capabilities.
Experience the nostalgia of arcade gaming with modern socket programming techniques.

![Python](https://img.shields.io/badge/Python-3.8%252B-blue)
![Socket Programming](https://img.shields.io/badge/Socket-Programming-green)
![Multiplayer](https://img.shields.io/badge/Multiplayer-Real--time-orange)
![Games](https://img.shields.io/badge/Games-3%2520Types-red)

---

## 🌟 Features

### 🎯 Game Library
- **Tic-Tac-Toe** → Classic 3x3 grid strategy game with an intuitive 1-9 input system.
- **Rock-Paper-Scissors** → Instant decision-based gameplay with real-time results.
- **Number Guessing Duel** → Turn-based number prediction game with hints.

### 🏗️ Architecture
- **Real-time Multiplayer** → Socket-based networking for a seamless gameplay experience.
- **Lobby System** → Automatic player matching and dedicated game sessions.
- **Score Management** → Comprehensive individual and session-based scoring.
- **Game History** → Complete persistent record of all matches played.
- **Colorful Terminal UI** → Rich ANSI-colored interface for an enhanced user experience.

---

## 🛠️ Technology Stack
- **Python 3.8+** → Core programming language with standard library modules.
- **Socket Programming** → Raw socket implementation for network communication.
- **Multithreading** → Concurrent client handling and game session management.
- **ANSI Escape Codes** → Advanced terminal formatting and colored output.
- **UUID Generation** → Unique session identification for lobbies.

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git version control system

### Quick Start

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Arnavgl/Terminal-Multiplayer-Arcade.git](https://github.com/Arnavgl/Terminal-Multiplayer-Arcade.git)
    ```

2.  **Navigate to the source directory**
    ```bash
    cd Terminal-Multiplayer-Arcade/src
    ```
    *No additional dependencies are needed - it uses pure Python!*

3.  **Start the game server**
    ```bash
    python server.py
    ```

4.  **In separate terminal windows, connect clients**
    ```bash
    python client.py
    ```

---

## 🚀 Usage

### Server Configuration
The server runs on `localhost:5555` by default. To customize, edit `server.py`:

```python
# In server.py
HOST = 'your-host-address'  # Change for network access
PORT = your-port-number     # Change if 5555 is occupied
````

### Client Connection

Clients automatically connect to the server and enter the matchmaking queue. The system supports multiple concurrent game lobbies.

### Game Flow

  - **Connection** → Clients connect to the server and wait for an opponent.
  - **Matchmaking** → Players are automatically paired into dedicated game lobbies.
  - **Game Selection** → Player 1 chooses from the available games.
  - **Gameplay** → Real-time turn-based gameplay.
  - **Scoring** → Points are awarded and displayed after each match.
  - **Continuation** → Players can choose to play different games in the same lobby.

-----

## 🎮 Game Details

### 🟦 Tic-Tac-Toe

  - **Input System** → Numbered grid (1-9) for intuitive positioning.
  - **Visual Feedback** → Dimmed numbers on the board show available moves.
  - **Win Detection** → All 8 possible win conditions are implemented.
  - **Draw Detection** → Automatic stalemate recognition.

### ✊✋✌️ Rock-Paper-Scissors

  - **Simple Commands** → Natural language input (rock/paper/scissors).
  - **Instant Results** → Immediate outcome calculation and display.
  - **Validation** → Input sanitization and error handling for invalid moves.

### 🔢 Number Guessing

  - **Turn-Based** → Alternating guessing system between two players.
  - **Smart Hints** → "Too high" / "too low" feedback to guide players.
  - **Range** → Numbers are chosen between 1-100 for balanced gameplay.

-----

## 📁 Project Structure

```bash
Terminal-Multiplayer-Arcade/
├── src/
│   ├── server.py               # Main server with lobby management
│   ├── client.py               # Client application and UI
│   ├── game_utils.py           # Shared utilities and constants
│   ├── tic_tac_toe.py          # Tic-Tac-Toe game implementation
│   ├── rock_paper_scissors.py  # RPS game implementation
│   └── number_guessing.py      # Number guessing game implementation
├── docs/
│   ├── README.md               # This file
│   └── ARCHITECTURE.md         # Technical documentation
├── requirements.txt            # Project dependencies (if any)
└── .gitignore                  # Git exclusion rules
```

-----

## 🔧 Technical Implementation

### Network Architecture

**Server Components**

  - **Socket Server** → Handles all incoming client connections.
  - **Lobby Manager** → Creates, manages, and terminates game sessions.
  - **Thread Pool** → Handles concurrent client communication for non-blocking gameplay.
  - **Game Registry** → Manages the available game types that can be played.

**Client Components**

  - **Connection Handler** → Manages all communication with the server.
  - **Input Processor** → Handles user input and validation.
  - **Display Manager** → Renders the game UI, boards, and messages in the terminal.

### 🎨 Color System

A simple class is used to manage ANSI color codes for a rich and intuitive UI.

```python
# ANSI Color Codes Implementation
class Colors:
    RED = '\033[91m'     # Error messages and losses
    GREEN = '\033[92m'   # Success messages and wins
    BLUE = '\033[94m'    # Player 1 elements
    MAGENTA = '\033[95m' # Headers and highlights
    # ... more colors for a rich UI
```

-----

## 🤝 Contributing

We welcome contributions\! Please feel free to submit pull requests for:

  - New game implementations
  - UI/UX improvements
  - Performance optimizations
  - Documentation enhancements
  - Bug fixes and stability improvements

### Development Setup

1.  **Fork and clone the repository**
    ```bash
    git clone [https://github.com/YourUsername/Terminal-Multiplayer-Arcade.git](https://github.com/YourUsername/Terminal-Multiplayer-Arcade.git)
    ```
2.  **Create a feature branch**
    ```bash
    git checkout -b feature/your-awesome-feature
    ```
3.  **Make your changes and test thoroughly.**
4.  **Submit a pull request with a detailed description of your changes.**

⭐ If you find this project interesting, please give it a star on GitHub\!

-----

🕹️ Experience the perfect blend of classic gaming nostalgia and modern networking technology with **Terminal Multiplayer Arcade**\!

```
```