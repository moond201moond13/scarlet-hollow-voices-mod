# Scarlet Hollow voice pack installer. Downloads the voice files from Hugging Face
# into game\voice. Safe to stop and run again: finished parts are skipped.
$ErrorActionPreference = "Stop"
$Base = "https://huggingface.co/datasets/moond13/scarlet-hollow-voices/resolve/main"
$Root = $PSScriptRoot

if (-not (Test-Path (Join-Path $Root "ScarletHollow.exe"))) {
    throw "Put this folder's files next to ScarletHollow.exe (the game folder), then run Install.bat again."
}
$Game  = Join-Path $Root "game"
$Voice = Join-Path $Game "voice"
$State = Join-Path $Game "voice_pack_state"
$Temp  = Join-Path $Root "voice_download"
foreach ($d in @($Voice, $State, $Temp)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$manifestPath = Join-Path $Temp "manifest.json"
Write-Host "Getting the file list..."
& curl.exe -L --fail --retry 5 -s -o $manifestPath "$Base/manifest.json"
if ($LASTEXITCODE -ne 0) { throw "Could not download the file list. Check your internet connection." }
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$shards = @($manifest.shards)
$totalGB = [math]::Round((($shards | Measure-Object -Property bytes -Sum).Sum) / 1GB, 1)
Write-Host ("Voice pack: {0} parts, about {1} GB to download. You need about twice that free on this drive while installing." -f $shards.Count, $totalGB)

$i = 0
foreach ($s in $shards) {
    $i++
    $name = $s.name
    $marker = Join-Path $State ($name + ".done")
    if (Test-Path $marker) { Write-Host "[$i/$($shards.Count)] $name already installed"; continue }
    $zip = Join-Path $Temp $name
    Write-Host "[$i/$($shards.Count)] Downloading $name ..."
    & curl.exe -L --fail --retry 5 -C - -o $zip "$Base/$name"
    if ($LASTEXITCODE -ne 0) { throw "Download of $name failed. Run Install.bat again to resume." }
    if ((Get-Item $zip).Length -ne [int64]$s.bytes) { throw "$name is the wrong size. Delete the voice_download folder and run Install.bat again." }
    Write-Host "[$i/$($shards.Count)] Unpacking $name ..."
    & tar.exe -xf $zip -C $Voice
    if ($LASTEXITCODE -ne 0) { throw "Could not unpack $name." }
    Set-Content -Path $marker -Value "ok"
    Remove-Item $zip -Force
}
Remove-Item $Temp -Recurse -Force -ErrorAction SilentlyContinue
$count = (Get-ChildItem $Voice -Filter *.wav).Count
Write-Host "Done. $count voice files are in game\voice."
