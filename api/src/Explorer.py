from mesa import Agent, Model


class Explorer(Agent):
    RANDOM_SEED = 12345

    def __init__(self, unique_id: int, model: Model) -> None:
        """
        Initializes a new instance of the agent

        Args:
            unique_id (int): Unique identifier of the agent
            model (Model): Model in which the agent is instantiated
        """

        super().__init__(unique_id, model)
        self.random.seed(self.RANDOM_SEED)
        self.type = "explorer"
        self.visited = set()

    def move(self) -> None:
        """
        Moves the agent in a random walk, prioritizing unvisited cells.
        """

        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        unvisited_neighbors = [
            cell
            for cell in neighbors
            if cell not in self.visited and self.model.grid.is_cell_empty(cell)
        ]

        if unvisited_neighbors:
            new_pos = self.random.choice(unvisited_neighbors)

        else:
            empty_neighbors = [
                cell for cell in neighbors if self.model.grid.is_cell_empty(cell)
            ]

            if empty_neighbors:
                new_pos = self.random.choice(empty_neighbors)

            else:
                return  # No move if no empty cells are available

        self.model.grid.move_agent(self, new_pos)
        self.visited.add(new_pos)

    def find_food(self) -> None:
        """
        Look for food in in the current cell and mark it in the known food layer.
        """

        (x, y) = self.pos

        self.model.known_food_layer[x][y] = self.model.food_layer[x][y]

    def find_storage(self) -> None:
        """
        Look for storage in the current cell and mark it in the known storage layer.
        """

        (x, y) = self.pos

        if self.model.storage_location == (x, y):
            self.model.known_storage_location = (x, y)

    def step(self) -> None:
        """
        Step through the environment.
        """

        self.move()
        self.find_food()
        self.find_storage()
