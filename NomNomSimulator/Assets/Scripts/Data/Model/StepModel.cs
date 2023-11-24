using System;
using System.Collections.Generic;

[Serializable]
public class StepModel
{
    public int id;
    public List<AgentModel> agents;
    public List<FoodModel> food;
}