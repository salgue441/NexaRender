using System.Collections.Generic;

[System.Serializable]
public class Simulation
{
    public int steps;
    public StorageModel storage_location;
    public List<StepModel> agent_positions; 
    public List<FoodModel> food_positions;
}
