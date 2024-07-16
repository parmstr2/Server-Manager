$headers = @{
    "Content-Type" = "application/json"
}

$data = @{
    "ip" = "192.168.2.19"
    "port" = 25566
    "version" = "1.21"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/new/minecraft/test" -Method POST -Headers $headers -Body $data