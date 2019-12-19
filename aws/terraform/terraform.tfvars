key_name = "iwase-key"
#public_key_path = "~/.ssh/AWS_EC2_01.pub"
public_key_path = "~/.ssh/id_rsa.pub"

app_name = "uma"
root_segment = "10.10.0.0/16"
private_segment1 = "10.10.1.0/24"
private_segment2 = "10.10.2.0/24"

db_ami = "ami-06d51e91cea0dac8d" # Ubuntu 18.04 LTS official ami
db_instance = "t2.micro"
uma_processed_ip = "10.10.1.10"

dataprocessor_count = "1" # 20 % dataprocessor_count = 0
#dataprocessor_count = "20" # 20 % dataprocessor_count = 0
dataprocessor_ami = "ami-06d51e91cea0dac8d" # Ubuntu 18.04 LTS official ami
dataprocessor_instance = "t2.micro"

