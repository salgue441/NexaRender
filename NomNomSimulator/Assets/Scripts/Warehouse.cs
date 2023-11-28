using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Warehouse : MonoBehaviour
{
    /// <summary>
    /// Sets the warehouse's position.
    /// </summary>
    public void Appearance(int x, int z)
    {
        transform.position = new Vector3(x, 0.2f, z);
    }
}
