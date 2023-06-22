$connectionString = "<your connection string>"
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "<your path>"
$watcher.Filter = "*.*"
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

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
Register-ObjectEvent $watcher "Created" -Action $action

while ($true) {sleep 5}