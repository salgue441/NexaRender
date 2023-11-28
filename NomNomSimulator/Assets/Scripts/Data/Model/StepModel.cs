using System;
using System.Collections.Generic;

/// <summary>
/// Model for the step.
/// </summary>
[Serializable]
public class StepModel
{
    public int id;
    public List<AgentModel> agents;
    public List<FoodModel> food;
    public PickedFoodModel food_picked = null;
}