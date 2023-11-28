from mesa import Agent, Model
import numpy as np


class Collector(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        """
        Creates a new instance of a Collector agent

        Args:
            unique_id (int): The unique identifier of the agent
            model (Model): The model the agent belongs to
        """
        super().__init__(unique_id, model)
        self.random.seed(12345)
        self.has_food = False
        self.type = "collector"

    def step(self) -> None:
        """
        Step function for the agent
        """

        self.find_storage()

        if not self.has_food and not self.storage_found():
            self.random_move()
            return

        self.move_to_food()
        self.move_to_storage()

    def move_to_food(self) -> None:
        """
        Moves the agent to the food location
        """

        if self.ready_to_pick() == False:
            return

        target = self.find_closest_food()
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=1
        )

        if target is None:
            self.random_move()
            return

        if self.pos == target:
            self.pick_food()
            return

        self.move(target, neighborhood)

    def move_to_storage(self) -> None:
        """
        Moves the agent to the storage location
        """

        if self.ready_to_drop() == False:
            return

        target = self.model.known_storage_location
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=1
        )

        if self.pos == target:
            self.drop_food()
            return

        self.move(target, neighborhood)

    def pick_food(self) -> None:
        """
        Pick food at the current location if the agent is ready to pick food
        """

        (x, y) = self.pos
        self.model.known_food_layer[x][y] = 0
        self.model.food_layer[x][y] = 0
        self.has_food = True
        self.model.picking_steps.append(
            {
                "id_collector": self.unique_id[1],
                "x": x,
                "y": y,
                "step": self.model.schedule.steps,
                "picked": True,
            }
        )

    def drop_food(self) -> None:
        """
        Drop food at the storage location
        """

        self.has_food = False
        self.model.storaged_food += 1
        self.random_move()

    def random_move(self) -> None:
        """
        Moves the agent randomly
        """

        new_pos = self.random.choice(
            self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False, radius=1
            )
        )

        self.model.grid.move_agent(self, new_pos)

    def move(self, target: tuple, neighborhood: tuple) -> None:
        """
        Moves the agent
        """

        pos_array = np.array(self.pos)
        target_array = np.array(target)
        direction = np.sign(target_array - pos_array)

        new_pos = np.clip(
            pos_array + direction,
            [0, 0],
            [self.model.grid.width - 1, self.model.grid.height - 1],
        )

        new_pos = tuple(new_pos)
        max_tries = 10

        while self.model.grid.get_cell_list_contents(new_pos) and max_tries > 0:
            new_pos = tuple(self.random.choice(neighborhood))
            max_tries -= 1

        if max_tries > 0:
            self.model.grid.move_agent(self, new_pos)
            self.pos = new_pos

    # Helpers
    def find_storage(self) -> None:
        """
        Look for storage in the current cell and mark it in the known storage layer.
        """

        (x, y) = self.pos
        if self.model.storage_location == (x, y):
            self.model.known_storage_location = (x, y)

    def find_closest_food(self) -> None:
        """
        Find the closest food location

        Returns:
            None
        """

        food_positions = np.argwhere(self.model.known_food_layer == 1)
        if not food_positions.size:
            return None

        distances = np.sum(np.abs(food_positions - np.array(self.pos)), axis=1)
        return tuple(food_positions[np.argmin(distances)])

    def distance_to(self, position: tuple) -> int:
        """
        Find the distance to a position

        Args:
            position (tuple): The position to find the distance to

        Returns:
            int: The distance to the position
        """

        return np.sum(np.abs(np.array(self.pos) - np.array(position)))

    def storage_found(self) -> bool:
        """
        Check if the agent has found the storage location

        Returns:
            bool: True if the agent has found the storage location, False otherwise
        """

        return self.model.known_storage_location is not None

    def ready_to_pick(self) -> bool:
        """
        Check if the agent is ready to pick food. Agent is ready to pick if:
        - There is food in the food layer
        - The agent does not have food
        - The storage location is found

        Returns:
            bool: True if the agent is ready to pick food, False otherwise
        """

        return (
            np.any(self.model.known_food_layer)
            and not self.has_food
            and self.storage_found()
        )

    def ready_to_drop(self) -> bool:
        """
        Check if the agent is ready to drop food. Agent is ready to drop if:
        - The agent has food
        - The storage location is found

        Returns:
            bool: True if the agent is ready to drop food, False otherwise
        """

        return self.has_food and self.storage_found()
