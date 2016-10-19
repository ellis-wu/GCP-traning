#!/usr/bin/env python
import json
import sys
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def gcp_credential():
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('compute', 'v1', credentials=credentials)
        return service
    except:
        sys.exit("Promise Undefined.")


def gcp_instance_list(project, zone):
    # region = 'asia-east1'
    try:
        request = gcp_credential().instances().list(project=project, zone=zone)
        response = request.execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit("instance list error")


def gcp_instance_get(project, zone, instance):
    try:
        request = gcp_credential().instances().get(project=project, zone=zone, instance=instance)
        response = request.execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit("instance get error")


def gcp_instance():
    if len(sys.argv) < 3:
        sys.exit('Usage: gcpclient instance {list|get}')
    else:
        if sys.argv[2] == 'list':
            if len(sys.argv) != 5:
                message_alert(
                    "Usage: gcpclient instance list {project_id} {zone}",
                    "list project instance infomation"
                )
            else:
                # 'test-project-146302', 'asia-east1-a'
                project = sys.argv[3]
                zone = sys.argv[4]
                gcp_instance_list(project, zone)
        elif sys.argv[2] == 'get':
            if len(sys.argv) != 6:
                message_alert(
                    "Usage: gcpclient instance get {project_id} {zone} {instance}",
                    "get instance infomation"
                )
            else:
                project = sys.argv[3]
                zone = sys.argv[4]
                instance = sys.argv[5]
                gcp_instance_get(project, zone, instance)
        else:
            sys.exit('Usage: gcpclient instance {list|get}')


def message_alert(usage, description):
    print("{usage:<70} \t {description:<50}".format(
        usage=usage,
        description=description
    ))


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: gcpclient {instance}')
    else:
        if sys.argv[1] == 'instance':
            gcp_instance()



if __name__ == '__main__':
    main()
