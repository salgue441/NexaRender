using UnityEngine;
using System.Collections;
using System;
using System.Collections.Generic;


/// <summary>
/// Manages the behavior of a collector agent, including its appearance
/// and movement within the simulation environment.
/// </summary>
public class Collector : MonoBehaviour
{
    public AgentModel agent;
    public int id;
    private Animator animator;
    public GameObject waffle;
    private SimManager simManager;
    GameObject[] gameObjects;

    // Constructor
    /// <summary>
    /// Creates a new instance of Collector:: class.
    /// </summary>
    /// <param name="id">The ID of the agent to be spawned</param>
    public Collector(string id, SimManager manager)
    {
        this.simManager = manager;
    }

    /// <summary>
    /// Initializes the animator for the explorer.
    /// </summary>
    void Awake()
    {
        animator = GetComponent<Animator>();
        waffle = transform.FirstOrDefault(x => x.CompareTag("MouthWaffle")).gameObject;
    }

    /// <summary>
    /// Handles the spawning of the agent in the simulat    ion environment.
    /// </summary>
    /// <param name="x">The x-coordinate of the agent's spawn location</param>
    /// <param name="z">The z-coordinate of the agent's spawn location</param>
    public void Appearance(int x, int z)
    {
        transform.position = new(x, 0.6f, z);
    }

    /// <summary>
    /// Handles the movement of the agent in the simulation environment.
    /// </summary>
    /// <param name="x">The x-coordinate of the agent's destination</param>
    /// <param name="z">The z-coordinate of the agent's destination</param>
    public void Move(int x, int z, float speed, bool hasFood)
    {
        animator.Play("Walk");
        StartCoroutine(MoveToPosition(new(x, 0.6f, z), speed));

        if (!hasFood)
        {
            gameObjects = GameObject.FindGameObjectsWithTag("Waffle");
            // print gameObjects
            foreach (GameObject gameObject in gameObjects)
            {
                if(x == gameObject.transform.position.x && z == gameObject.transform.position.z) {
                    Destroy(gameObject);
                    break;
                }
                    
            }

            waffle.SetActive(false);
        }
        else
        {
            waffle.SetActive(true);
        }
    }

    /// <summary>
    /// Moves the agent to a specified position in the simulation environment.
    /// Allows for the agent to move in a smooth, linear fashion.
    /// </summary>
    /// <param name="target">The position to move the agent to</param>
    /// <param name="duration">The duration of the movement</param>
    /// <returns></returns>
    IEnumerator MoveToPosition(Vector3 target, float duration)
    {
        float time = 0;
        Vector3 startPosition = transform.position;

        while (time < duration)
        {
            // Calculate the direction to the target
            Vector3 direction = (target - startPosition).normalized;

            // Check if the direction is not zero before rotating
            if (direction != Vector3.zero)
            {
                // Rotate towards the target
                Quaternion toRotation = Quaternion.LookRotation(direction);
                transform.rotation = Quaternion.Slerp(transform.rotation, toRotation, Time.deltaTime * 5f);
            }

            // Move towards the target
            transform.position = Vector3.Lerp(startPosition, target, time / duration);

            time += Time.deltaTime;
            yield return null;
        }

        // Ensure the collector is facing the final destination
        transform.LookAt(target);
        transform.position = target;
    }

    // void OnTriggerEnter(Collider other)
    // {
    //     if (other.gameObject.CompareTag("Waffle") && hasFood)
    //     {
    //         Destroy(other.gameObject);
    //         waffle.SetActive(true);
    //     }
    //     if (other.gameObject.CompareTag("Warehouse"))
    //     {
    //         waffle.SetActive(false);
    //     }
    // }
}