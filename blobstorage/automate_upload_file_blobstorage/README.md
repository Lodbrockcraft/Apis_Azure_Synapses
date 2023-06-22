# Automates uploading files to Blob Storage from a local folder

# Information this project

In lake house projects we often need to work with files of various specific formats. Sometimes these files are in the cloud like sharepoint or google drive, but in some cases these files may be in a local folder on the user's machine. When we are faced with the second case, we need to develop solutions to move these files to some cloud repository. Often, just a folder synchronization configuration with sharepoit or google drive would solve it, it would be a simpler way out to solve the problem, but what do we do when we cannot use this solution?
In this project I present a solution that I developed that automates sending files from a local folder to an Azure Blob Storage.
Well, enough rambling, let's get down to business.

## Configure the environment

In this solution I am using PowerShell language.
If you use a Windows machine, by default PowerShell is already installed and ready to use. The only thing you need to do is install the library that we are going to use in the solution, in this case azcopy.

To install azcopy you need to run the following command in PowerShell command prompt.

```bash
Invoke-WebRequest -Uri 'https://azcopyvnext.azureedge.net/release20220315/azcopy_windows_amd64_10.14.1.zip' -OutFile 'azcopyv10.zip'
Expand-archive -Path '.\azcopyv10.zip' -Destinationpath '.\'
$AzCopy = (Get-ChildItem -path '.\' -Recurse -File -Filter 'azcopy.exe').FullName
# Invoke AzCopy 
& $AzCopy
```

To confirm that the installation was successful, just run the command below.

```bash
azcopy --help
```

If the command was not recognized, you will need to set environment variables.
Follow that documentation https://renicius-pagotto.medium.com/azcopy-copiando-dados-para-o-azure-blob-storage-7e49103fee41.

# Connection string Blob Storage

To generate the connection string, use this documentation.
- https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/create-sas-tokens?view=form-recog-3.0.0
- https://learn.microsoft.com/pt-br/azure/storage/common/storage-sas-overview

In this project we use a Blob SAS URL, generated directly from the container where the files will be stored.

This line creates a FileSystemWatcher object that monitors changes to a directory.
```bash
$watcher = New-Object System.IO.FileSystemWatcher
```

This line defines if you want to include subdirectories in the monitoring.
```bash
$watcher.IncludeSubdirectories = $true
```
This line activates monitoring.
```bash
$watcher.EnableRaisingEvents = $true
```

This is the action that will be performed when a file is added to the monitored directory. It takes the full path of the added file and uses AzCopy to copy it to the specified destination.
```bash
$action = {
    $path = $Event.SourceEventArgs.FullPath
    $changeType = $Event.SourceEventArgs.ChangeType
    $logline = "$(Get-Date), $changeType, $path"
    # Removes all hidden Zone.Identifier files from the folder before pushing the file to the blob.
    Remove-Item $path -Stream Zone.Identifier
    Write-Host $logline

    # Use AzCopy to upload the file to Azure Blob Storage
    azcopy copy $path $connectionString --overwrite=prompt --from-to=LocalBlob --blob-type BlockBlob --follow-symlinks --check-length=true --put-md5 --follow-symlinks --disable-auto-decoding=false --recursive --log-level=INFO
}
```

This line logs an event for when a file is added to the monitored directory. It calls the action defined above.
```bash
Register-ObjectEvent $watcher "Created" -Action $action
```
This loop keeps the script running indefinitely.
```bash
while ($true) {sleep 5}
```

# Documentation used
- https://renicius-pagotto.medium.com/azcopy-copiando-dados-para-o-azure-blob-storage-7e49103fee41
- https://learn.microsoft.com/pt-br/azure/storage/common/storage-use-azcopy-files
- https://stackoverflow.com/questions/55643403/powershell-script-to-copy-files-from-server-to-azure-blob-container
