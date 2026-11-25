resource "aws_vpc" "project" {
  cidr_block           = "10.71.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "cloud-vpc-grp01"
  }
}

# Adopt this project's default NACL and remove AWS's allow-all defaults.
# No workloads run in either subnet, so deny-all is safe for this demo.
resource "aws_default_network_acl" "project" {
  default_network_acl_id = aws_vpc.project.default_network_acl_id
  subnet_ids             = [aws_subnet.public.id, aws_subnet.private.id]
  tags = {
    Name = "cloud-acl-default-grp01"
  }
}

# An internet route makes this subnet public; no instance is launched here.
resource "aws_internet_gateway" "project" {
  vpc_id = aws_vpc.project.id
  tags = {
    Name = "cloud-igw-grp01"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.project.id
  cidr_block              = "10.71.10.0/24"
  availability_zone       = "eu-west-3a"
  map_public_ip_on_launch = false
  tags = {
    Name = "cloud-subnet-public-grp01"
  }
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.project.id
  cidr_block              = "10.71.20.0/24"
  availability_zone       = "eu-west-3a"
  map_public_ip_on_launch = false
  tags = {
    Name = "cloud-subnet-private-grp01"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.project.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.project.id
  }
  tags = {
    Name = "cloud-routes-public-grp01"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.project.id
  tags = {
    Name = "cloud-routes-private-grp01"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# The VPC default Security Group is managed with zero ingress and egress.
resource "aws_default_security_group" "project" {
  vpc_id = aws_vpc.project.id
  tags = {
    Name = "cloud-sg-default-grp01"
  }
}

resource "aws_security_group" "public" {
  name        = "cloud-sg-public-grp01"
  description = "No inbound admin access; only local HTTPS egress"
  vpc_id      = aws_vpc.project.id
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.project.cidr_block]
    description = "Project VPC HTTPS only"
  }
  tags = {
    Name = "cloud-sg-public-grp01"
  }
}

resource "aws_security_group" "private" {
  name        = "cloud-sg-private-grp01"
  description = "No inbound admin access; only local HTTPS egress"
  vpc_id      = aws_vpc.project.id
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.project.cidr_block]
    description = "Project VPC HTTPS only"
  }
  tags = {
    Name = "cloud-sg-private-grp01"
  }
}
