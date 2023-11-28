using System;
using UnityEngine;

public static class TransformEx
{
    /// <summary>
    /// Returns the first child transform that matches the query.
    /// </summary>
    /// <param name="transform">The transform to search.</param>
    /// <param name="query">The query to match.</param>
    /// <returns>The first child transform that matches the query.</returns>
    public static Transform FirstOrDefault(
        this Transform transform, Func<Transform, bool> query)
    {
        if (query(transform))
            return transform;

        for (int i = 0; i < transform.childCount; i++)
        {
            var result = FirstOrDefault(transform.GetChild(i), query);
            if (result != null)
                return result;
        }

        return null;
    }
}