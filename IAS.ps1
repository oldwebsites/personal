$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

$DownloadURL = 'https://raw.githubusercontent.com/oldwebsites/personal/refs/heads/main/IAS.cmd'

$rand = Get-Random -Maximum 99999999
$isAdmin = [bool]([Security.Principal.WindowsIdentity]::GetCurrent().Groups -match 'S-1-5-32-544')
$FilePath = if ($isAdmin) { "$env:SystemRoot\Temp\IAS_$rand.cmd" } else { "$env:TEMP\IAS_$rand.cmd" }

# 下载文件
Write-Host "正在从你的仓库获取脚本..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $DownloadURL -OutFile $FilePath -UseBasicParsing

# 运行脚本
Start-Process $FilePath -Wait

# 清理痕迹
if (Test-Path $FilePath) { Remove-Item $FilePath -Force }
Write-Host "执行完成且已清理临时文件。" -ForegroundColor Green
