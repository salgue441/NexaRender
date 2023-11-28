using System;

/// <summary>
/// Model for the agent.
/// </summary>
[Serializable]
public class AgentModel
{
    public int id;
    public string type;
    public int x;
    public int y;
    public bool has_food;
}