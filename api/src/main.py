from mesa import Model
from Model import NomNomModel
import pandas as pd

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
    """

    model = NomNomModel(GRID_SIZE, GRID_SIZE, NUM_AGENTS, MAX_FOOD)

    for _ in range(ITERATIONS):
        model.step()
        if model.storaged_food == MAX_FOOD:
            break
    print(f"Simulation finished in {model.schedule.steps} steps")
    return model


def get_data(model):
    steps = []
    all_positions = model.datacollector.get_model_vars_dataframe()

    storage_location = {
        "x": model.storage_location[0],
        "y": model.storage_location[1]
    }
    agent_positions = all_positions["Agent Positions"]
    food_positions = all_positions["Food Positions"]

    for i in range(len(agent_positions)):
        for j in range(len(model.picking_steps)):
            if model.picking_steps[j]["step"] == i:
                food_picked = model.picking_steps[j]
                break
            else:
                food_picked = None
        steps.append({
            "id": i,
            "agents": agent_positions[i],
            "food": food_positions[i], 
            "food_picked": food_picked
        })

    return {
        "storage_location": storage_location,
        "steps": steps,
        "total_steps": model.schedule.steps
    }

def main():
    model = run_simulation()
    data = get_data(model)
    return data

if __name__ == "__main__":
    main()