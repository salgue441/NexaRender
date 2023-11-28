from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np

from Explorer import Explorer
from Collector import Collector


class NomNomModel(Model):
    RANDOM_SEED = 12345

    __slots__ = (
        "schedule",
        "grid",
        "running",
        "food_layer",
        "known_food_layer",
        "storage_location",
        "datacollector",
    )

    def __init__(self, width: int, height: int, num_agents=5, max_food=47) -> None:
        """
        Initializes the model with the given parameters.

        Args:
            width (int): The width of the grid.
            height (int): The height of the grid.
            num_agents (int): The number of agents to be created.
            max_food (int): The maximum amount of food to be created.
        """

        self.random.seed(self.RANDOM_SEED)

        # Data Collector
        self.datacollector = DataCollector(
            {
                "Food": lambda m: np.sum(m.food_layer),
                "Known Food": lambda m: np.sum(m.known_food_layer),
                "Agents": lambda m: m.schedule.get_agent_count(),
                "Agent Positions": self.get_positions,
                "Food Positions": self.get_food_positions,
                "Warehouse location": lambda m: m.storage_location,
            }
        )

        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(width, height, False)
        self.running = True
        self.total_food_spawned = 0

        # Layers
        self.taken_food_positions = set()
        self.picking_steps = []
        self.init_food_layer = np.zeros((width, height), dtype=np.int8)
        self.food_layer = np.zeros((width, height), dtype=np.int8)
        self.known_food_layer = np.zeros((width, height), dtype=np.int8)
        self.known_storage_location = None
        self.storage_location = None
        self.storaged_food = 0
        self.num_food = max_food

        # Model Instances
        self.spawn_food(self.num_food)
        self.place_warehouse()
        self.spawn_agents(3, Collector, "collector_")
        self.spawn_agents(2, Explorer, "explorer_")

    def spawn_agents(
        self, num_agents: int, agent_class: Agent, prefix: str = ""
    ) -> None:
        """
        Spawns the agents in random places of the grid.

        Args:
            num_agents (int): The number of agents to be created.
            agent_class (Agent): The class of the agent to be created.
        """

        for i in range(num_agents):
            attempts = 0
            max_attempts = 10

            while attempts < max_attempts:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

                if self.grid.is_cell_empty((x, y)):
                    agent = agent_class((prefix, i), self)
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)
                    break

                attempts += 1

    def spawn_food(self, max_food: int) -> None:
        """
        Spawns the food in random places of the grid between 2 to 5 cells with
        one food item. The interval between the spawns is 5 steps.

        Args:
            max_food (int): The maximum amount of food to be created.
        """

        suitable_cells = [
            (x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if self.grid.is_cell_empty((x, y))
            and self.food_layer[x][y] == 0
            and (x, y) != self.storage_location
        ]

        num_food_to_spawn = min(
            self.random.randrange(2, 6),
            max_food - self.total_food_spawned,
            len(suitable_cells),
        )

        for _ in range(num_food_to_spawn):
            if suitable_cells:
                x, y = self.random.choice(suitable_cells)
                self.food_layer[x][y] = 1
                self.init_food_layer[x][y] = 1
                self.total_food_spawned += 1
                suitable_cells.remove((x, y))

    def place_warehouse(self) -> None:
        """
        Places the warehouse in the center of the grid.
        """

        while True:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            if self.grid.is_cell_empty((x, y)) and self.food_layer[x][y] == 0:
                self.storage_location = (x, y)
                break

    def step(self) -> None:
        """
        Advances the model by one step. Spawns the food each 5 steps
        """

        self.schedule.step()
        self.datacollector.collect(self)

        # Spawn food each 5 steps
        if self.schedule.steps % 5 == 0:
            self.spawn_food(self.num_food)

    def get_positions(model: Model) -> list:
        """
        Get the positions of the agents in the grid

        Args:
            model (Model): The model instance to get the agent positions from

        Returns:
            list: List of agent positions
        """

        agent_positions = []

        for agent in model.schedule.agents:
            agent_positions.append(
                {
                    "id": agent.unique_id[1],
                    "x": agent.pos[0],
                    "y": agent.pos[1],
                    "type": agent.unique_id[0],
                    "has_food": agent.type == "collector" and agent.has_food,
                }
            )

        return agent_positions

    def get_food_positions(model: Model) -> list:
        """
        Get the positions of the food in the grid

        Args:
            model (Model): The model instance to get the food positions from

        Returns:
            list: List of food positions
        """
        food_positions = []

        for x in range(model.grid.width):
            for y in range(model.grid.height):
                value = model.food_layer[x][y]
                if value == 1 and (x, y) not in model.taken_food_positions:
                    new_pos = {
                        "x": x,
                        "y": y,
                    }
                    food_positions.append(new_pos)
                    model.taken_food_positions.add((x, y))

        return food_positions
