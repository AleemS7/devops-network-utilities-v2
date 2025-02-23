############################
#   Azure Provider Setup   #
############################
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "azurerm" {
  features {}
}

############################
#   Resource Group         #
############################
resource "azurerm_resource_group" "rg" {
  name     = "devops-network-rg"
  location = "eastus"
}

############################
#   Azure Kubernetes       #
############################
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "devops-network-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "devopsnetwork"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }
}

############################
#   Azure Container Reg    #
############################
resource "azurerm_container_registry" "acr" {
  name                = "devopsnetworkacr${random_integer.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "random_integer" "suffix" {
  min = 10000
  max = 99999
}

############################
#   Grant AKS Pull Access  #
############################
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

############################
#   Outputs                #
############################
output "resource_group_name" {
  description = "Name of the resource group."
  value       = azurerm_resource_group.rg.name
}

output "aks_name" {
  description = "AKS cluster name."
  value       = azurerm_kubernetes_cluster.aks.name
}

output "acr_name" {
  description = "ACR registry name."
  value       = azurerm_container_registry.acr.name
}
