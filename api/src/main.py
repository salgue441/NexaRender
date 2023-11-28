from mesa import Model
from Model import NomNomModel
import numpy as np

NUM_AGENTS = 5
MAX_FOOD = 47
GRID_SIZE = 20
FOOD_SPAWN_INTERVAL = 5
MIN_FOOD_PER_SPAWN = 2
MAX_FOOD_PER_SPAWN = 5
ITERATIONS = 1500


def run_simulation() -> Model:
    """
    Runs the simulation.

    Returns:
        Model: The model object.
    """

    model = NomNomModel(GRID_SIZE, GRID_SIZE, NUM_AGENTS, MAX_FOOD)

    while model.storaged_food < MAX_FOOD:
        model.step()

    print(f"Simulation finished in {model.schedule.steps} steps")
    return model


def get_data(model) -> dict:
    """
    Gets the data from the model.

    Args:
        model (Model): The model object.

    Returns:
        dict: The data from the model.
    """

    steps = []
    all_positions = model.datacollector.get_model_vars_dataframe()

    storage_location = {"x": model.storage_location[0], "y": model.storage_location[1]}
    agent_positions = all_positions["Agent Positions"]
    food_positions = all_positions["Food Positions"]

    # Convert picking steps to a dictionary for quick lookup
    picking_steps_dict = {step["step"]: step for step in model.picking_steps}

    num_agent_positions = len(agent_positions)
    for i in range(num_agent_positions):
        # Directly get the food picked if it exists in the dictionary
        food_picked = picking_steps_dict.get(i)

        steps.append(
            {
                "id": i,
                "agents": agent_positions[i],
                "food": food_positions[i],
                "food_picked": food_picked,
            }
        )

    return {
        "storage_location": storage_location,
        "steps": steps,
        "total_steps": model.schedule.steps,
    }


def main():
    model = run_simulation()
    data = get_data(model)
    return data


if __name__ == "__main__":
    main()
