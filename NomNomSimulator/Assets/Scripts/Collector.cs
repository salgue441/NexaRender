using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Collector : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        int randomXPosition = Mathf.RoundToInt(UnityEngine.Random.Range(0.0f, 20.0f));
        int randomZPosition = Mathf.RoundToInt(UnityEngine.Random.Range(0.0f, 20.0f));

        transform.position = new Vector3(randomXPosition, 0.6f, randomZPosition);

        Vector3 currentPosition = transform.position;
    }

    public void Move(int x, int z)
    {
        transform.position = new Vector3(x, 0.6f, z);
    }
}
