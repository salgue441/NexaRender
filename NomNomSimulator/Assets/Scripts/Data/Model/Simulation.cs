using System.Collections.Generic;

/// <summary>
/// Model for the simulation.
/// </summary>
[System.Serializable]
public class Simulation
{
    public int total_steps;
    public StorageModel storage_location;
    public List<StepModel> steps; 
}
