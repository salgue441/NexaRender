using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading;

public class Collector : MonoBehaviour
{
    public AgentModel agent;

    public Collector(string id)
    {
        this.agent = new AgentModel();
        this.agent.id = id;
        this.agent.type = "collector";
    }
    public void Appearance(int x, int z)
    {
        // Aparecer en la posición inicial
        transform.position = new Vector3(x, 0.6f, z);
    }

    public void Move(int x, int z)
    {
        transform.position = new Vector3(x, 0.6f, z);
    }

}
