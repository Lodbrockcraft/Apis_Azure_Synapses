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
    while ((Test-Path -Path $path) -and (IsFileLocked -Path $path)) {
        Start-Sleep -Seconds 1
    }
    # Removes all hidden Zone.Identifier files from the folder before pushing the file to the blob.
    Remove-Item $path -Stream Zone.Identifier
    Write-Host $logline
    # Use AzCopy to upload the file to Azure Blob Storage
    azcopy copy $path $connectionString --overwrite=prompt --from-to=LocalBlob --blob-type BlockBlob --follow-symlinks --check-length=true --put-md5 --follow-symlinks --disable-auto-decoding=false --recursive --log-level=INFO
}
Register-ObjectEvent $watcher "Created" -Action $action
# check if the file is locked
function IsFileLocked {
    param([string]$Path)

    try {
        $file = New-Object System.IO.FileInfo $Path
        $stream = $file.Open([System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)

        if ($stream) {
            $stream.Close()
        }
        return $false
    }
    catch {
        return $true
    }
}
while ($true) {sleep 5}
