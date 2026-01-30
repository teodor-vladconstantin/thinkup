
# PowerShell script to run the migration with credential prompt

Write-Host "AWS -> ScyllaDB Migration Helper" -ForegroundColor Cyan
Write-Host "--------------------------------"

$use_env = Read-Host "Do you have valid AWS credentials in your .env file already? (y/n)"

if ($use_env -eq 'n') {
    Write-Host "Please enter your AWS credentials (these will be used for this session only):"
    $access_key = Read-Host "AWS Access Key ID"
    $secret_key = Read-Host "AWS Secret Access Key"
    $session_token = Read-Host "AWS Session Token (Optional, press Enter to skip)"
    $region = Read-Host "AWS Region [default: eu-central-1]"

    if ([string]::IsNullOrWhiteSpace($region)) {
        $region = "eu-central-1"
    }

    $env:AWS_ACCESS_KEY_ID = $access_key
    $env:AWS_SECRET_ACCESS_KEY = $secret_key
    if (-not [string]::IsNullOrWhiteSpace($session_token)) {
        $env:AWS_SESSION_TOKEN = $session_token
    }
    $env:AWS_REGION = $region
    $env:AWS_DEFAULT_REGION = $region
}

# Ensure destination is set to local Scylla
$env:DYNAMODB_ENDPOINT_URL = "http://localhost:8000"

# Install requirements quietly
Write-Host "Checking dependencies..."
pip install boto3 tqdm python-dotenv --quiet

# Run Python script
Write-Host "Starting migration script..." -ForegroundColor Green
python scripts/migrate_to_scylla.py
