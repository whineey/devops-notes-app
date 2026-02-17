variable "location" {
  default = "francecentral"
}

variable "vm_size" {
  default = "Standard_B1s"
}

variable "admin_username" {
  default = "azureuser"
}

variable "ssh_admin_public_key_path" {
  description = "Path to SSH public key"
  default     = "~/.ssh/id_ed25519.pub"
}

variable "ssh_deploy_public_key_path" {
  description = "Path to 'deploy' user public key"
  default     = "~/.ssh/deploy_key.pub"
}