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
    public GameObject FoodPrefab;
    public int collectedFood = 0;

    private readonly Simulation sim = APIHelper.GetSimulation();
    private Queue<StepModel> simulationSteps;
    private bool isSimulationRunning = false;
    private float normalTimeScale = 3f;
    private float acceleratedTimeScale = 30f;
    private bool isAccelerated = false;

    /// <summary>
    /// Initializes the simulation environment.
    /// </summary>
    private void Start()
    {
        Time.timeScale = normalTimeScale;
        warehouse.Appearance(sim.storage_location.x, sim.storage_location.y);
        InitializeAgents();

        simulationSteps = new Queue<StepModel>(sim.steps);
        isSimulationRunning = true;

        StartCoroutine(MoveAgents());
    }

    /// <summary>
    /// Initializes the agents in the simulation environment.
    /// </summary>
    private void InitializeAgents()
    {
        if (sim.steps.Count > 0)
        {
            StepModel firstStep = sim.steps[0];

            int collector_count = 0;
            int explorer_count = 0;

            foreach (AgentModel agent in firstStep.agents)
            {
                if (agent.type == "collector_")
                    collector[collector_count++].Appearance(agent.x, agent.y);

                else
                    explorer[explorer_count++].Appearance(agent.x, agent.y);
            }
        }
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            isAccelerated = !isAccelerated;
            Time.timeScale = isAccelerated ? acceleratedTimeScale : normalTimeScale;
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

        foreach (AgentModel agent in step.agents)
        {
            if (agent.type == "collector_")
                collector[collector_count++].Move(agent.x, agent.y, speed, step);

            else if (agent.type == "explorer_")
                explorer[explorer_count++].Move(agent.x, agent.y, speed);

        }

        if (step.id % 5 == 0)
            foreach (FoodModel food in step.food)
            {
                // rotate the food in x 90 degrees
                GameObject newFood = Instantiate(FoodPrefab, new Vector3(food.x, 0.64f, food.y), Quaternion.Euler(90, 0, 0));
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

    public void CollectFood()
    {
        collectedFood++;
    }

}

