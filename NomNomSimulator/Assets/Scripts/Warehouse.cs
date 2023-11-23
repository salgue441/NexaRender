using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Warehouse : MonoBehaviour
{
    public void Appearance(int x, int z)
    {
        // Aparecer en la posición inicial
        transform.position = new Vector3(x, 0.2f, z);
    }
}
