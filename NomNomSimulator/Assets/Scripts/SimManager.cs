using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimManager : MonoBehaviour
{
    Simulation sim = APIHelper.GetSimulation();

    // print to console simulation data
    void Start()
    {
        Debug.Log("Simulation steps: " + sim.steps);
        Debug.Log("Simulation storage location: (" + sim.storage_location.x + ", " + sim.storage_location.y + ")");
        Debug.Log("Simulation food positions: ");
        foreach (FoodModel food in sim.food_positions)
        {
            Debug.Log("(" + food.x + ", " + food.y + ") Value: " + food.value);
        }
        Debug.Log("Simulation agent positions: ");
        foreach (StepModel step in sim.agent_positions)
        {
            Debug.Log("Step: " + step.step);
            foreach (AgentModel agent in step.positions)
            {
                Debug.Log("Agent: " + agent.id + " (" + agent.x + ", " + agent.y + ")" + " Type: " + agent.type);
            }
        }
    }
}

