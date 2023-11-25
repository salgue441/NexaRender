from mesa import Agent, Model
import numpy as np


class Collector(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
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

        if self.pos == target:
            self.pick_food()
            return

        self.move(target, neighborhood)

    def move_to_storage(self) -> None:
        """
        Moves the agent to the storage location
        """

        if not self.ready_to_drop():
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
        for i in range(self.model.grid.width):
            for j in range(self.model.grid.height):
                if self.model.known_food_layer[i][j] == 1:
                    self.model.known_food_layer[i][j] = 0
                    self.model.food_layer[i][j] = 0
                    self.has_food = True
                    return

    def drop_food(self) -> None:
        """ "
        Drop food at the storage location
        """

        self.has_food = False
        self.model.storaged_food += 1
        self.random_move()

    def random_move(self) -> None:
        """
        Moves the agent randomly
        """

        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=1
        )

        self.move(self.random.choice(neighborhood), neighborhood)

    def move(self, target: tuple, neighborhood: tuple) -> None:
        """
        Moves the agent
        """

        x = target[0] - self.pos[0]
        y = target[1] - self.pos[1]

        x = 1 if x > 0 else -1 if x < 0 else 0
        y = 1 if y > 0 else -1 if y < 0 else 0

        # Check if the new position is within the grid
        if self.pos[0] + x < 0 or self.pos[0] + x >= self.model.grid.width:
            x = 0
        if self.pos[1] + y < 0 or self.pos[1] + y >= self.model.grid.height:
            y = 0

        # Choose a new position closer to the target
        new_pos = (self.pos[0] + x, self.pos[1] + y)
        cellmate = self.model.grid.get_cell_list_contents(new_pos)

        max_tries = 10
        while cellmate:
            new_pos = self.random.choice(neighborhood)
            cellmate = self.model.grid.get_cell_list_contents(new_pos)
            max_tries -= 1
            if max_tries == 0:
                return

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

        food_positions = []

        for i in range(self.model.grid.width):
            for j in range(self.model.grid.height):
                if self.model.known_food_layer[i][j] == 1:
                    food_positions.append((i, j))

        closest_food = None
        closest_distance = 1000000

        for food_position in food_positions:
            distance = self.distance_to(food_position)
            if distance < closest_distance:
                closest_food = food_position
                closest_distance = distance

        return closest_food

    def distance_to(self, position: tuple) -> int:
        """
        Find the distance to a position

        Args:
            position (tuple): The position to find the distance to

        Returns:
            int: The distance to the position
        """

        return abs(self.pos[0] - position[0]) + abs(self.pos[1] - position[1])

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

        food_found = np.sum(self.model.known_food_layer)
        return food_found > 0 and not self.has_food and self.storage_found()

    def ready_to_drop(self) -> bool:
        """
        Check if the agent is ready to drop food. Agent is ready to drop if:
        - The agent has food
        - The storage location is found

        Returns:
            bool: True if the agent is ready to drop food, False otherwise
        """

        return self.has_food and self.storage_found()
