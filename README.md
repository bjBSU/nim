# Game of NIM with reinforcement learning

# Summary
The peremise of this project was to create a reinforcement learning model and train it to learn the strategies of the game of NIM. Once the model was trained, it would be implemented into a cutsom ReTiCo module. This ReTiCo module, along with the Misty module and others, would be connected in a pipeline that would allow the Misty robot to play the interactive game with a human player. Misty would be using ReTiCo's vision, Misty_camera and YOLOv8 modules to detect objects infront of the robot, and use that data to see the current state of the game. Misty would then play games with the player by processing the objects it detects and feedinng that information to the module and then to the model to derive the best move for the current state of the game. 

# Files
RL_Agent : This is the file that contains the data for the Reinforcement learning agent using in Gymnasium.

nim_env :  This is the file that contains the environment for the reinforcement learning agent to train and learn in.

nim_script : This is the jupyter notebook file that contains how the model was built, trained, and tuned from the agent and the environment.

nim-1 : This is the pickle file that hold the trained model and metadata about the parameters.

misty_runner : This is the runner file that connects all the different ReTiCo modules together, ie. how the camera footage gets processed and detected objects get sent to the nim module.

retico_nim : This is the custom ReTiCo module for the game of Nim that connects and controls the Misty robot. While also recieving and processing the detected objects information from the ReTiCo vision module.
