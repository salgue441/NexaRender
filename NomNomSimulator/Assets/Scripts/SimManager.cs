using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading;

public class SimManager : MonoBehaviour
{
    public Warehouse warehouse;
    public List<Collector> collector;
    public List<Explorer> explorer;
    public Food food;

    private readonly Simulation sim = APIHelper.GetSimulation();
    private Queue<StepModel> simulationSteps;
    private bool isSimulationRunning = false;

    /// <summary>
    /// Initializes the simulation environment.
    /// </summary>
    private void Start()
    {
        Time.timeScale = 3f;
        warehouse.Appearance(sim.storage_location.x, sim.storage_location.y);
        InitializeAgents();

        simulationSteps = new Queue<StepModel>(sim.positions);
        isSimulationRunning = true;

        StartCoroutine(MoveAgents());
    }

    /// <summary>
    /// Initializes the agents in the simulation environment.
    /// </summary>
    private void InitializeAgents()
    {
        if (sim.positions.Count > 0)
        {
            StepModel firstStep = sim.positions[0];

            int collector_count = 0;
            int explorer_count = 0;

            foreach (AgentModel agent in firstStep.positions)
            {
                if (agent.type == "collector_")
                    collector[collector_count++].Appearance(agent.x, agent.y);

                else
                    explorer[explorer_count++].Appearance(agent.x, agent.y);
            }
        }
    }

    /// <summary>
    /// Processes a step in the simulation.
    /// </summary>
    private void ProcessStep(StepModel step)
    {
        int explorer_count = 0;
        int collector_count = 0;
        float speed = 1f;

        foreach (AgentModel agent in step.positions)
        {
            if (agent.type == "collector_")
                collector[collector_count++].Move(agent.x, agent.y, speed);

            else if (agent.type == "explorer_")
                explorer[explorer_count++].Move(agent.x, agent.y, speed);
            
        }
    }

    /// <summary>
    /// Moves the agents in the simulation environment.
    /// </summary>
    /// <returns></returns>
    /// <remarks>
    /// This coroutine is used to move the agents in the simulation environment.
    /// </remarks>

    IEnumerator MoveAgents()
    {
        while (isSimulationRunning)
        {
            if (simulationSteps.Count > 0)
            {
                ProcessStep(simulationSteps.Dequeue());
            }

            yield return new WaitForSeconds(1f);
        }
    }
}

