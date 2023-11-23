using System.Collections.Generic;

[System.Serializable]
public class Simulation
{
    public int steps;
    public StorageModel storage_location;
    public List<StepModel> positions; 
}
