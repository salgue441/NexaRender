using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Manages the behavior of an explorer agent in the simulation.
/// </summary>
public class Explorer : MonoBehaviour
{
    public AgentModel agent;
    private Animator animator;

    /// <summary>
    /// Initializes the Explorer with an ID.
    /// </summary>
    /// <param name="id">The unique identifier for the explorer.</param>

    public Explorer(string id)
    {
        this.agent = new AgentModel();
        this.agent.id = id;
        this.agent.type = "explorer_";
    }

    /// <summary>
    /// Initializes the animator for the explorer.
    /// </summary>
    void Awake()
    {
        animator = GetComponent<Animator>();
    }

    /// <summary>
    /// Sets the initial appearance of the explorer at a specific position.
    /// </summary>
    /// <param name="x">The x-coordinate of the explorer's initial position.</param>
    /// <param name="z">The z-coordinate of the explorer's initial position.</param>
    public void Appearance(int x, int z)
    {
        transform.position = new Vector3(x, 0.6f, z);
    }

    /// <summary>
    /// Moves the explorer to a new position.
    /// </summary>
    /// <param name="x">The x-coordinate of the new position.</param>
    /// <param name="z">The z-coordinate of the new position.</param>
    public void Move(int x, int z, float speed)
    {
        animator.Play("Fly");
        StartCoroutine(MoveToPosition(new Vector3(x, 0.6f, z), speed));
    }

    /// <summary>
    /// Coroutine to move the explorer to a specified position in the simulation environment.
    /// </summary>
    /// <param name="target">The position to move the explorer to.</param>
    /// <param name="duration">The duration of the movement.</param>
    /// <returns></returns>
    IEnumerator MoveToPosition(Vector3 target, float duration)
    {
        float time = 0;
        Vector3 startPosition = transform.position;

        while (time < duration)
        {
            // Calculate the direction to the target
            Vector3 direction = (target - startPosition).normalized;

            // Rotate towards the target
            Quaternion toRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, toRotation, Time.deltaTime * 5f);

            // Move towards the target
            transform.position = Vector3.Lerp(startPosition, target, time / duration);

            time += Time.deltaTime;
            yield return null;
        }

        // Ensure the collector is facing the final destination
        transform.LookAt(target);
        transform.position = target;
    }
}
