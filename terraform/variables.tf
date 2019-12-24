provider "aws" {
    version = "~> 2.0"
    region  = "us-west-2"
}

variable "key_name" {
    description = "Desired name of AWS key pair"
}

variable "public_key_path" {
    description = <<DESCRIPTION
    Path to the SSH public key to be used for authentication.
    Ensure this keypair is added to your local SSH agent so provisioners can
    connect.

    Example: ~/.ssh/terraform.pub
    DESCRIPTION
}

variable "app_name" {}
variable "root_segment" {}
variable "private_segment1" {}
variable "private_segment2" {}

variable "db_ami" {}
variable "db_instance" {}
variable "uma_processed_ip" {}

variable "dataprocessor_count" {}
variable "dataprocessor_ami" {}
variable "dataprocessor_instance" {}

