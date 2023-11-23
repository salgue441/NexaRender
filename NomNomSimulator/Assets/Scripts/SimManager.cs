using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimManager : MonoBehaviour
{
    public Collector collector;
    // public Explorer explorer;
    public Warehouse warehouse;
    public Food food;

    public int totalSteps = 10;

    void Start()
    {
        // Llamar a la función que inicializa la simulación
        InitializeSimulation(); 
    }

    void Update()
    {
        // Llamar a la función que realiza los pasos de simulación en cada frame
        SimulateStep();
    }

    void InitializeSimulation()
    {
        warehouse.Appearance(3, 13);
    }

    void SimulateStep()
    {
        
    }
}
