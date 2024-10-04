"""
InputManager class to handle keyboard and joystick inputs for a game.
Attributes:
    joystick (pygame.joystick.Joystick): The joystick object if a joystick is connected.
    actions (dict): Dictionary to store the current state of actions.
    previous_actions (dict): Dictionary to store the previous state of actions.
Methods:
    __init__():
        Initializes the InputManager, setting up the joystick and action dictionaries.
    handle_input(events):
        Updates the actions dictionary based on the current key states and joystick inputs.
    get_actions():
        Returns the current action states.
    was_pressed(action):
        Checks if an action was just pressed.
"""

import pygame


class InputManager:
    def __init__(self):
        # Initialize joystick
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Dictionary to store the current actions
        self.actions = {
            "move_left": False,
            "move_right": False,
            "move_up": False,
            "move_down": False,
            "attack": False,
            "magic": False,
            "pause": False,
            "next_spell": False,
            "previous_spell": False,
            "help": False,
        }
        # Store previous actions to detect key presses
        self.previous_actions = self.actions.copy()

    def handle_input(self, events):
        """Update the actions dictionary based on the current key states."""
        self.previous_actions = self.actions.copy()
        keys = pygame.key.get_pressed()
        self.actions["move_left"] = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.actions["move_right"] = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.actions["move_up"] = keys[pygame.K_UP] or keys[pygame.K_w]
        self.actions["move_down"] = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.actions["attack"] = keys[pygame.K_SPACE]
        self.actions["magic"] = keys[pygame.K_f]

        # Reset triggers for cycling spells
        self.actions["next_spell"] = False
        self.actions["previous_spell"] = False

        # Cycling spells with Q and E
        if keys[pygame.K_q]:
            self.actions["previous_spell"] = True
        if keys[pygame.K_e]:
            self.actions["next_spell"] = True

        # Controller input
        if self.joystick:
            # Left stick for movement
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)
            deadzone = 0.1
            self.actions["move_left"] = axis_x < -deadzone
            self.actions["move_right"] = axis_x > deadzone
            self.actions["move_up"] = axis_y < -deadzone
            self.actions["move_down"] = axis_y > deadzone

            # R1 for sword attack
            self.actions["attack"] = self.joystick.get_button(5)  # Button index for R1

            # L1 for magic
            self.actions["magic"] = self.joystick.get_button(4)  # Button index for L1

            # L2 and R2 for cycling magic spells
            if self.joystick.get_button(6):  # L2 button
                self.actions["previous_spell"] = True
            if self.joystick.get_button(7):  # R2 button
                self.actions["next_spell"] = True

            # Pause button (Options button on PS5 controller)
            if self.joystick.get_button(9):
                self.actions["pause"] = True

        # For actions like pause and help, we need to detect key presses
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.actions["pause"] = True
                elif event.key == pygame.K_h:
                    self.actions["help"] = True  # New action for help menu

    def get_actions(self):
        """Return the current action states."""
        return self.actions

    def was_pressed(self, action):
        """Check if an action was just pressed."""
        return not self.previous_actions.get(action, False) and self.actions.get(action, False)

