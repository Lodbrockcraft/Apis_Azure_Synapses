# Documentation
# https://learn.microsoft.com/pt-br/powershell/module/az.synapse/update-azsynapsesparkpool?view=azps-9.7.1&viewFallbackFrom=azps-9.7.0#code-try-8

# Inform the spark pool version
Get-AzSynapseSparkPool -WorkspaceName yourWorkspaceName -Name yoursparkpoolname | Select-Object -Property SparkVersion

# Spark pool update to the version you want
# In this example it is updating to version 3.3
Update-AzSynapseSparkPool -WorkspaceName yourWorkspaceName -Name yoursparkpoolname -SparkVersion 3.3