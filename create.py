# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");

import argparse
import sys
from typing import Dict

import backoff
from google.cloud import container_v1


def on_success(details: Dict[str, str]) -> None:
    """
    """
    print("Successfully created cluster after {elapsed:0.1f} seconds".format(**details))


def on_failure(details: Dict[str, str]) -> None:
    """
    """
    print(" Creating time elapsed {wait:0.1f}".format(**details))


@backoff.on_predicate(
    # the backoff algorithm to use. we use exponential backoff here
    backoff.expo,
    # the test function on the return value to determine if a retry is necessary
    lambda x: x != container_v1.Operation.Status.DONE,
    # maximum number of times to retry before giving up
    max_tries=20,
    # function to execute upon a failure and when a retry a scheduled
    on_backoff=on_failure,
    # function to execute upon a successful attempt and no more retries needed
    on_success=on_success,
)
def poll_for_op_status(
    client: container_v1.ClusterManagerClient, op_id: str
) -> container_v1.Operation.Status:

    op = client.get_operation({"name": op_id})
    return op.status


def create_cluster(project_id: str, location: str, cluster_name: str) -> None:
    """Create a new GKE cluster in the given GCP Project and Zone"""
    # Initialize the Cluster management client.
    client = container_v1.ClusterManagerClient()
    # Create a fully qualified location identifier of form `projects/{project_id}/location/{zone}'.
    cluster_location = client.common_location_path(project_id, location)
    cluster_def = {
        "name": cluster_name,
        "initial_node_count": 1,
        "node_config": {"machine_type": "e2-micro"},
    }
    # Create the request object with the location identifier.
    request = {"parent": cluster_location, "cluster": cluster_def}
    create_response = client.create_cluster(request)
    op_identifier = f"{cluster_location}/operations/{create_response.name}"
    # poll for the operation status and schedule a retry until the cluster is created
    poll_for_op_status(client, op_identifier)
# [END gke_create_cluster]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("zone", help="GKE Cluster zone")
    parser.add_argument("cluster_name", help="Name to be given to the GKE Cluster")
    args = parser.parse_args()

    if len(sys.argv) != 4:
        parser.print_usage()
        sys.exit(1)

    create_cluster(args.project_id, args.zone, args.cluster_name)