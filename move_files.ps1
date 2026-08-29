# ===== CONFIGURE THESE TWO PATHS =====
$sourceDir = "N:\My Documents\Programming\Fun Coffee\bosses\123456"   # folder that contains the xxxxxxxx subfolders
$destDir   = "D:\Projects\fun_coffee_data\bosses\123456"      # new folder where all renamed files will go
# =====================================

# Create destination folder if it doesn't exist
New-Item -ItemType Directory -Path $destDir -Force | Out-Null

# Process every subfolder
Get-ChildItem -Path $sourceDir -Directory | ForEach-Object {
    $folderName = $_.Name

    # Move + rename every file inside this subfolder
    Get-ChildItem -Path $_.FullName -File | ForEach-Object {
        $newName  = "$folderName-$($_.Name)"          # e.g. xxxxxxxx-yyy.jpg
        $destPath = Join-Path $destDir $newName

        Move-Item -Path $_.FullName -Destination $destPath -Force
        Write-Host "Moved: $($_.Name)  →  $newName"
    }
}

Write-Host "`nDone!"