using System.Collections.Generic;

[System.Serializable]
public class Simulation
{
    public int total_steps;
    public StorageModel storage_location;
    public List<StepModel> steps; 
}
