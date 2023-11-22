from mesa import Model
from Model import NomNomModel

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
    all_positions = model.datacollector.get_model_vars_dataframe()

    storage_location = model.storage_location
    agent_pos = all_positions["Agent Positions"]
    food_positions = model.init_food_layer
    steps = model.schedule.steps

    return {
        "storage_location": storage_location,
        "agent_pos": agent_pos,
        "food_positions": food_positions,
        "steps": steps
    }

def main():
    model = run_simulation()
    data = get_data(model)
    print(data)

if __name__ == "__main__":
    main()