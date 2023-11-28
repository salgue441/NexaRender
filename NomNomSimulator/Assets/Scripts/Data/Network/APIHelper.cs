using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;

/// <summary>
/// Helper class for the API.
/// </summary>
public static class APIHelper
{
    /// <summary>
    /// Gets the simulation.
    /// </summary>
    /// <returns>The simulation.</returns>
    public static Simulation GetSimulation()
    {
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create(
            "http://localhost:8585");

        HttpWebResponse response = (HttpWebResponse) request.GetResponse();
        StreamReader reader = new StreamReader(response.GetResponseStream());
        string json = reader.ReadToEnd();

        return JsonUtility.FromJson<Simulation>(json);
    }
}