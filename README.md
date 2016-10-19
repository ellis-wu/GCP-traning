# GCP Example

GCP APIs example.

## Before running

1. If not already done, enable the Compute Engine API
   and check the quota for your project at
   [https://console.developers.google.com/apis/api/compute](https://console.developers.google.com/apis/api/compute)

2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   [https://cloud.google.com/sdk/](https://cloud.google.com/sdk/) and run
   ```sh
   $ gcloud beta auth application-default login
   ```

3. Install the Python client library for Google APIs by running
   ```sh
   $ pip install --upgrade google-api-python-client
   ```

## Starting

> 請以管理者權限進行操作！

顯示專案中所有 instance 的資訊：
```sh
$ ./gcpclient instance list {project_id} {zone}
```

取得 instance 的資訊：
```sh
$ ./gcpclient instance get {project_id} {zone} {instance}
```
