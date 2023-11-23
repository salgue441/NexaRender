using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading;

public class SimManager : MonoBehaviour
{
    Simulation sim = APIHelper.GetSimulation();
    public Warehouse warehouse;
    public List<Collector> collector;
    public List<Explorer> explorer;
    public Food food;

    void Start()
    {
        int explorer_count = 0;
        int collector_count = 0;

        warehouse.Appearance(sim.storage_location.x, sim.storage_location.y);

        foreach (FoodModel food in sim.food_positions)
        {
            //Debug.Log("(" + food.x + ", " + food.y + ") Value: " + food.value);
        }

        foreach (StepModel step in sim.agent_positions)
        {
            explorer_count = 0;
            collector_count = 0;
            foreach (AgentModel agent in step.positions)
            {
                if (step.step == 0)
                {
                    if (agent.type == "collector_")
                    {
                        collector[collector_count++].Appearance(agent.x, agent.y);
                    }
                    else if (agent.type == "explorer_")
                    {
                        explorer[explorer_count++].Appearance(agent.x, agent.y);
                    }
                }
            }
        }
    }
}

