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

__*請以管理者權限進行操作！*__

> 若遇到 `Google Application Default Credentials` 問題，請參考：[Google Application Default Credentials](https://developers.google.com/identity/protocols/application-default-credentials)

顯示專案中所有 instance 的資訊：
```sh
$ ./gcpclient instance list {project_id} {zone}
```

取得 instance 的資訊：
```sh
$ ./gcpclient instance get {project_id} {zone} {instance}
```

建立一個基本的 `debian-8` instance：
```sh
$ ./gcpclient instance create {project_id} {zone} {instance_id}
```
