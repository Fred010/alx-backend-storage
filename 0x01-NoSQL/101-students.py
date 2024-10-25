#!/usr/bin/env python3
""" returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.
    """
    # Using MongoDB's aggregation framework to compute average and sort
    pipeline = [
        {
            "$addFields": {
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    # Run the aggregation pipeline
    return list(mongo_collection.aggregate(pipeline))
