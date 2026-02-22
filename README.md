# Flappy Bird AI using NEAT

This repository contains a **Flappy Bird AI** powered by the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. The AI learns to play the game by evolving neural networks through generations, with each generation getting better at passing pipes and surviving longer.

## Overview

This project uses **NEAT** to evolve a population of neural networks that control birds in a simple **Flappy Bird** game. The network decides whether the bird should jump based on inputs such as the bird's position relative to the pipes.

## Demo

Check out the AI in action! Here's a demo of the trained model playing Flappy Bird:

https://github.com/user-attachments/assets/56b17a39-52e2-45a5-afd4-c24c7ee50357    

## Features

- **NEAT algorithm**: Used to evolve neural networks over generations.
- **Pygame**: For game rendering and mechanics.
- **Live Plotting**: Tracks the best and mean scores across generations.
- **Flexible configurations**: Customize the network and game parameters for various experiments.

## Tech Stack

- **Python**: The programming language used for development.
- **NEAT-Python**: Library for the NEAT algorithm.
- **Pygame**: For rendering and game mechanics.
- **Matplotlib**: For visualizing the training progress.

## 📂 Project Structure

```
FlappyBird-AI/
│── imgs/                      # Directory containing game images (bird, pipes, background, etc.)
│── best_flappy_model.pkl      # Serialized file of the best trained neural network model
│── config                     # Configuration file defining NEAT parameters and settings
│── config_variables.py        # Python file containing game-specific variables (window size, colors, etc.)
│── flappy_trainer.py          # Script that runs the NEAT training loop and evaluates the neural networks
│── u/                         # Unknown directory, potentially containing utility files
│── high_score.txt             # Text file storing the highest score achieved during training
│── mam.py                     # Utility or experimental Python script (purpose unclear, review the file)
│── NNdraw.py                  # Script for visualizing and drawing the neural network architecture
│── Objects.py                 # Contains classes defining game objects (bird, pipes, base, etc.)
│── requirements.txt           # Lists all Python dependencies for the project
│── README.md                  # Project documentation, describing the project and setup instructions
```

---

## Installation

To get started with this project, clone the repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/yourusername/FlappyBird-AI.git
cd FlappyBird-AI
pip install -r requirements.txt
```

## Requirements

This project requires the following Python packages:

- `pygame==2.5.2`
- `neat-python==0.92`
- `matplotlib==3.8.4`

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## How It Works

- **NEAT Setup**: The neural network evolves with each generation, using the NEAT algorithm to modify its structure.

- **Fitness Function**: The bird's survival time and its score (how many pipes it passes) determine its fitness.

- **Game Mechanics**: Pygame is used to simulate the Flappy Bird game, including the movement of pipes, the bird's jumping action, and the game's scoring system.

## Training the AI

To start training the AI, run the following command:

```bash
python flappy_trainer.py
```

The training process will evolve neural networks that control the bird. The training progress can be viewed in real-time using a plot that shows the best and mean scores per generation.

## Special Notes

After many trials and errors, I discovered that `bird.y` was not required for making the jump decision. Initially, I removed it from the inputs, but for some reason, the model performed worse. So, I added it back but switched to **FS-NEAT** connection types.

Here are some observations:

- **FS-NEAT Sparse Evolution**: This connection method evolved better models over time, but it didn’t use the `y` position of the bird even though it was present in the input.

- **Partial Connections**: I tried different partial connection fractions like `0.0`, `0.1`, and `0.5`, but the results were similar to the baseline.

- **Crash Issue**: When I manually removed the `y` position from the input, the model crashed. I’m not sure why it crashes, so if anyone knows the cause, feel free to contact me via [LinkedIn](https://www.linkedin.com/in/singhrabhay) or [Gmail](mailto\:abhayr24564@gmail.com), or you can raise a pull request to fix it.

- **Full Connections**: Setting the connections to **full** causes the model to learn much faster, reaching the goal in just 3 or so generations. However, I prefer the model to be more efficient by reducing the number of inputs needed.

## Future Improvements

- **Efficiency**: I'm aiming to make the AI more efficient by reducing the number of required inputs while maintaining performance.

- **Better Neural Network Architectures**: Explore alternate NEAT configurations or neural network architectures for better results.

## License

This project is licensed under the **MIT License**.

Feel free to use and modify this project. Contributions are welcome!
