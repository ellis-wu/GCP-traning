#!/usr/bin/env python
import json
import sys
import magic
from googleapiclient import discovery
from googleapiclient import http
from oauth2client.client import GoogleCredentials

# project id = test-project-146302
# region = asia-east1
# zone = asia-east1-a

def gcp_credential(api):
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build(api, 'v1', credentials=credentials)
        return service
    except:
        sys.exit("Promise Undefined.")


def gcp_instance_list(project, zone):
    try:
        request = gcp_credential('compute').instances().list(project=project, zone=zone)
        response = request.execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit("instance list error")


def gcp_instance_get(project, zone, instance):
    try:
        request = gcp_credential('compute').instances().get(project=project, zone=zone, instance=instance)
        response = request.execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit("instance get error")


def gcp_instance_create(project, zone, instance_id):
    try:
        # Get the latest Debian Jessie image.
        image_response = gcp_credential('compute').images().getFromFamily(
            project='debian-cloud', family='debian-8').execute()
        source_disk_image = image_response['selfLink']
        # Configure the machine
        machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
        # Configure th instance name
        name = instance_id

        config = {
            'name': name,
            'machineType': machine_type,
            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],
            # Specify a network interface with NAT to access the public internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],
            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],
            # Metadata is readable from the instance and allows you to
            # pass configuration from deployment scripts to instances.
            "metadata": {
                "kind": "compute#metadata",
                "fingerprint": "-wmDBHKA7Qk="
            },
        }
        gcp_credential('compute').instances().insert(project=project, zone=zone, body=config).execute()
        print("create [%s] success" % name)
    except:
        sys.exit("create instance fail.")


def gcp_instance_delete(project, zone, instance_id):
    try:
        request = gcp_credential('compute').instances().delete(project=project, zone=zone, instance=instance_id)
        response = request.execute()
        print("delete [%s] success" % instance_id)
    except:
        sys.exit("delete instance fail.")


def gcp_instance():
    if len(sys.argv) < 3:
        sys.exit('Usage: gcpclient instance {list|get|create|delete}')
    else:
        if sys.argv[2] == 'list':
            if len(sys.argv) != 5:
                message_alert(
                    "Usage: gcpclient instance list {project_id} {zone}",
                    "list project instance infomation"
                )
            else:
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
        elif sys.argv[2] == 'create':
            if len(sys.argv) != 6:
                message_alert(
                    "Usage: gcpclient instance create {project_id} {zone} {instance_id}",
                    "create instance"
                )
            else:
                project = sys.argv[3]
                zone = sys.argv[4]
                instance_id = sys.argv[5]
                gcp_instance_create(project, zone, instance_id)
        elif sys.argv[2] == 'delete':
            if len(sys.argv) != 6:
                message_alert(
                    "Usage: gcpclient instance delete {project_id} {zone} {instance_id}",
                    "delete instance"
                )
            else:
                project = sys.argv[3]
                zone = sys.argv[4]
                instance_id = sys.argv[5]
                gcp_instance_delete(project, zone, instance_id)
        else:
            sys.exit('Usage: gcpclient instance {list|get|create|delete}')


def project_list():
    try:
        request = gcp_credential('cloudresourcemanager').projects()
        response = request.list().execute()
        encodedjson =  json.dumps(response['projects'], sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit("get project list fail.")


def project_create(name, project):
    try:
        config = {
            'project_id': project,
            'name': name
        }
        request = gcp_credential('cloudresourcemanager').projects()
        response = request.create(body=config).execute()
        print("create [%s] project success" % name)
    except:
        sys.exit("create project fail.")


def project_delete(project):
    try:
        request = gcp_credential('cloudresourcemanager').projects()
        response = request.delete(projectId=project).execute()
        print("delete [%s] success" % project)
    except:
        sys.exit("delete prject fail")


def gcp_project():
    if len(sys.argv) < 3:
        sys.exit('Usage: gcpclient project {list|create|delete}')
    else:
        if sys.argv[2] == 'list':
            if len(sys.argv) != 3:
                message_alert(
                    "Usage: gcpclient project list",
                    "list all project infomation"
                )
            else:
                project_list()
        elif sys.argv[2] == 'create':
            if len(sys.argv) != 5:
                message_alert(
                    "Usage: gcpclient project create {project name} {project ID}",
                    "create project"
                )
            else:
                name = sys.argv[3]
                project = sys.argv[4]
                project_create(name, project)
        elif sys.argv[2] == 'delete':
            if len(sys.argv) != 4:
                message_alert(
                    "Usage: gcpclient project delete {project ID}",
                    "delete project"
                )
            else:
                project = sys.argv[3]
                project_delete(project)
        else:
            sys.exit('Usage: gcpclient project {list|create|delete}')


def gs_bucket_list(project):
    try:
        request = gcp_credential('storage').buckets()
        response = request.list(project=project).execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit('list bucket fail.')


def gs_bucket_get(bucket):
    try:
        request = gcp_credential('storage').buckets()
        response = request.get(bucket=bucket).execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit('get bucket fail')


def gs_bucket_create(project, bucket):
    try:
        config = {
            'name': bucket
        }
        request = gcp_credential('storage').buckets()
        response = request.insert(project=project, body=config).execute()
        print("create [%s] bucket success" % bucket)
    except:
        sys.exit('create bucket fail')


def gs_bucket_delete(bucket):
    try:
        request = gcp_credential('storage').buckets()
        response = request.delete(bucket=bucket).execute()
        print("delete [%s] bucket success" % bucket)
    except:
        sys.exit('delete bucket fail')


def gs_bucket():
    if len(sys.argv) < 3:
        sys.exit('Usage: gcpclient bucket {list|get|create|delete}')
    else:
        if sys.argv[2] == 'list':
            if len(sys.argv) != 4:
                message_alert(
                    "Usage: gcpclient bucket list {project ID}",
                    "list project all bucket information"
                )
            else:
                project = sys.argv[3]
                gs_bucket_list(project)
        elif sys.argv[2] == 'get':
            if len(sys.argv) != 4:
                message_alert(
                    "Usage: gcpclient bucket get {bucket}",
                    "list bucket information"
                )
            else:
                bucket = sys.argv[3]
                gs_bucket_get(bucket)
        elif sys.argv[2] == 'create':
            if len(sys.argv) != 5:
                message_alert(
                    "Usage: gcpclient bucket create {project ID} {bucket}",
                    "create bucket"
                )
            else:
                project = sys.argv[3]
                bucket = sys.argv[4]
                gs_bucket_create(project, bucket)
        elif sys.argv[2] == 'delete':
            if len(sys.argv) != 4:
                message_alert(
                    "Usage: gcpclient bucket delete {bucket}",
                    "delete bucket"
                )
            else:
                bucket = sys.argv[3]
                gs_bucket_delete(bucket)
        else:
            sys.exit('Usage: gcpclient bucket {list|get|create|delete}')


def gs_object_list(bucket):
    try:
        request = gcp_credential('storage').objects()
        response = request.list(bucket=bucket).execute()
        encodedjson =  json.dumps(response, sort_keys=True, indent=4)
        print encodedjson
    except:
        sys.exit('list fail.')

def gs_object_upload(bucket, file, filename):
    try:
        body = {
            'name': filename,
        }
        mime = magic.Magic(mime=True)
        fileType = mime.from_file(file)
        with open(file, 'rb') as f:
            request = gcp_credential('storage').objects()
            response = request.insert(bucket=bucket, body=body,
                                      media_body=http.MediaIoBaseUpload(f, fileType)).execute()
        print("upload [%s] to [%s] success" % (filename, bucket))
    except:
        sys.exit('upload file fail')


def gs_object_delete(bucket, object):
    try:
        request = gcp_credential('storage').objects()
        response = request.delete(bucket=bucket, object=object).execute()
        print("delete [%s] success" % object)
    except:
        sys.exit("delete object fail")


def gs_object():
    if len(sys.argv) < 3:
        sys.exit('Usage: gcpclient object {list|upload|delete}')
    else:
        if sys.argv[2] == 'list':
            if len(sys.argv) != 4:
                message_alert(
                    "Usage: gcpclient object list {bucket}",
                    "list bucket all object information"
                )
            else:
                bucket = sys.argv[3]
                gs_object_list(bucket)
        elif sys.argv[2] == 'upload':
            if len(sys.argv) != 6:
                message_alert(
                    "Usage: gcpclient object upload {bucket} {file path} {file name}",
                    "upload file to bucket"
                )
            else:
                bucket = sys.argv[3]
                file_path = sys.argv[4]
                file_name = sys.argv[5]
                gs_object_upload(bucket, file_path, file_name)
        elif sys.argv[2] == 'delete':
            if len(sys.argv) != 5:
                message_alert(
                    "Usage: gcpclient object delete {bucket} {file name}",
                    "delete object file"
                )
            else:
                bucket = sys.argv[3]
                file_name = sys.argv[4]
                gs_object_delete(bucket, file_name)
        else:
            sys.exit('Usage: gcpclient object {list|upload|delete}')


def message_alert(usage, description):
    print("{usage:<70} \t {description:<50}".format(
        usage=usage,
        description=description
    ))


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: gcpclient {instance|project|bucket|object}')
    else:
        if sys.argv[1] == 'instance':
            gcp_instance()
        elif sys.argv[1] == 'project':
            gcp_project()
        elif sys.argv[1] == 'bucket':
            gs_bucket()
        elif sys.argv[1] == 'object':
            gs_object()
        else:
            sys.exit('Usage: gcpclient {instance|project|bucket|object}')


if __name__ == '__main__':
    main()
