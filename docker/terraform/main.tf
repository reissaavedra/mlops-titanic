terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "2.92.0"
    }
  }
}

provider "azurerm" {
  subscription_id = "a835a93a-0c78-4ef6-afeb-95c2eb3ec364"
  client_id       = "d957d55d-526f-4451-8a60-6a023fcc9a40"
  client_secret   = "UYy8Q~hCh3EoK~.uYKj4HzMZZan2dIicZjbwbds9"
  tenant_id       = "773b568b-532d-4b14-8fdd-d07b438a8e21"
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_storage_account" "example" {
  name                     = "storacctestml"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "example" {
  name                  = "contentestml"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}
