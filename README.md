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

4. Install the Python library Magic
   ```sh
  $ pip install python-magic
   ```

## Starting
* [project operation](#project-operation)
  * [list](#list)
  * [create](#create)
  * [delete](#delete)
* [instance operation](#instance-operation)
  * [list](#list-1)
  * [get](#get)
  * [create](#create-1)
  * [delete](#delete-1)
* [bucket operation](#bucket-operation)
  * [list](#list-2)
  * [get](#get-1)
  * [create](#create-2)
  * [delete](#delete-2)
* [object operation](#object-operation)
  * [list](#list-3)
  * [upload](#upload)
  * [delete](#delete-3)

> * __*請以管理者權限進行操作！*__
> * 若遇到 `Google Application Default Credentials` 問題，請參考：[Google Application Default Credentials](https://developers.google.com/identity/protocols/application-default-credentials)

## project operation
Project manager 相關操作

### list
顯示所有 Project 的資訊：
```sh
$ ./gcpclient project list
```

### create
建立一個新的 Project：
```sh
$ ./gcpclient project create {project name} {project ID}
```

> project_id 必須是唯一，不可重複。

### delete
刪除 project：
```sh
$ ./gcpclient project delete {project ID}
```

> Shutting down a project does not delete the project immediately and only requests deleting the project. The project will be deleted at some later time. For more information see the [Overview page](https://cloud.google.com/resource-manager/docs/overview#project_deletion).

## instance operation

GCP instance 相關操作

### list

顯示專案中所有 instance 的資訊：
```sh
$ ./gcpclient instance list {project_id} {zone}
```

### get
取得 instance 的資訊：
```sh
$ ./gcpclient instance get {project_id} {zone} {instance}
```
### create
建立一個基本的 `debian-8` instance：
```sh
$ ./gcpclient instance create {project_id} {zone} {instance_id}
```

### delete
刪除 Project 中已存在的 instance：
```sh
$ ./gcpclient instance delete {project_id} {zone} {instance_id}
```

## bucket operation
Cloud Storage bucket 相關操作

### list
顯示專案中所有 bucket 的資訊：
```sh
$ ./gcpclient bucket list {project ID}
```

### get
取得 bucket 的資訊：
```sh
$ ./gcpclient bucket get {bucket}
```

### create
建立一個新的 bucket：
```sh
$ ./gcpclient bucket create {project ID} {bucket}
```

### delete
刪除 bucket：
```sh
$ ./gcpclient bucket delete {bucket}
```

## object operation
Cloud Storage object 相關操作

### list
顯示 bucket 中所有 object 的資訊：
```sh
$ ./gcpclient object list {bucket}
```

### upload
上傳 object 至指定 bucket 中：
```sh
$ ./gcpclient object upload {bucket} {file path} {file name}
```

### delete
刪除指定 bucket 中的 object：
```sh
$ ./gcpclient object delete {bucket} {file name}
```
