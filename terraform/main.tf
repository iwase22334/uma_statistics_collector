#####################################
## ssh key
#####################################
resource "aws_key_pair" "auth" {
      key_name   = "${var.key_name}"
      public_key = "${file(var.public_key_path)}"
}

#####################################
## vpc
#####################################
resource "aws_vpc" "vpc_main" {
    cidr_block              = "${var.root_segment}"
    enable_dns_hostnames    = true
    enable_dns_support      = true
    instance_tenancy        = "default"

    tags = {
        Name = "${var.app_name}"
    }
}

resource "aws_subnet" "vpc_main-private-subnet1" {
    vpc_id                  = "${aws_vpc.vpc_main.id}"
    cidr_block              = "${var.private_segment1}"
    availability_zone       = "us-west-2a"

    tags = {
        Name = "${var.app_name} private-subnet1"
    }
}

resource "aws_eip" "elastic_ip" {
    instance = "${aws_instance.processed_db.id}"
    vpc = true
}

resource "aws_internet_gateway" "gateway" {
    vpc_id = "${aws_vpc.vpc_main.id}"
    tags = {
        Name = "gateway"
    }
}

#####################################
## routing
#####################################
resource "aws_route_table" "routingtable" {
    vpc_id = "${aws_vpc.vpc_main.id}"
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.gateway.id}"
    }
    tags = {
        Name = "my-route-table"
    }
}

resource "aws_route_table_association" "subnet-association" {
    subnet_id = "${aws_subnet.vpc_main-private-subnet1.id}"
    route_table_id = "${aws_route_table.routingtable.id}"
}

#####################################
## security group
#####################################
resource "aws_security_group" "default" {
    vpc_id      = "${aws_vpc.vpc_main.id}"
    name        = "terraform_security_group"
    description = "Used in the terraform"

    # SSH access from anywhere
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # psql access from anywhere
    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["10.10.1.0/24"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

#####################################
## instance 
#####################################
resource "aws_s3_bucket" "everydb2store" {
  bucket = "iwase22334-uma-everydb2store"
  acl    = "public-read"

  tags = {
    Name = "everydb2store"
    Role = "storage"
  }
}

resource "aws_instance" "processed_db" {
    ami               = "${var.db_ami}"
    instance_type     = "${var.db_instance}"

    availability_zone = "us-west-2a"
    vpc_security_group_ids = ["${aws_security_group.default.id}"]
    subnet_id         = "${aws_subnet.vpc_main-private-subnet1.id}"
    private_ip        = "${var.uma_processed_ip}"
    key_name          = "${aws_key_pair.auth.id}"

    associate_public_ip_address = "true"

    tags = {
        Name = "processed_db"
        Role = "processeddb"
    }
}

resource "aws_instance" "dataprocessor" {
    count = "${format("%d", var.dataprocessor_count)}"
    ami = "${var.dataprocessor_ami}"
    instance_type = "${var.dataprocessor_instance}"

    availability_zone = "us-west-2a"
    vpc_security_group_ids = ["${aws_security_group.default.id}"]
    subnet_id         = "${aws_subnet.vpc_main-private-subnet1.id}"
    private_ip        = "${format("10.10.1.1%02d", count.index + 1)}"
    key_name          = "${aws_key_pair.auth.id}"

    associate_public_ip_address = "true"

    tags = {
        Name = "${format("dataprocessor_%02d", count.index + 1)}"
        Role = "dataprocessor"
        Peer = "${var.uma_processed_ip}"
        FromDate = "${format("%d", 19900000 + count.index * (300000 / var.dataprocessor_count))}"
        ToDate = "${format("%d", 19900000 + (count.index + 1) * (300000 / var.dataprocessor_count) - 1)}"
    }
}
