using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Warehouse : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        int randomXPosition = Mathf.RoundToInt(UnityEngine.Random.Range(0.0f, 20.0f));
        int randomZPosition = Mathf.RoundToInt(UnityEngine.Random.Range(0.0f, 20.0f));

        transform.position = new Vector3(randomXPosition, 0.2f, randomZPosition);

        Vector3 currentPosition = transform.position;
    }


    // Update is called once per frame
    void Update()
    {

    }
}
