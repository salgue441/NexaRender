using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Collector : MonoBehaviour
{
    public Collector(int id)
    {
        // Aparecer en la posición inicial
        transform.position = new Vector3(3, 0.6f, 13);
    }

    public void Move(int x, int z)
    {
        transform.position = new Vector3(x, 0.6f, z);
    }
}
