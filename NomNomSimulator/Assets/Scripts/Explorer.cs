using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading;

public class Explorer : MonoBehaviour
{
    private int id;

    public Explorer(int id)
    {
        this.id = id;
    }
    public void Appearance(int x, int z)
    {
        // Aparecer en la posición inicial
        transform.position = new Vector3(x, 0.6f, z);
    }

    public void Move(int x, int z)
    {
        // Moverse a la posición indicada
        transform.position = new Vector3(x, 0.6f, z);
    }

}
