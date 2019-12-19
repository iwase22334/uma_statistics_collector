# uma_aws

* dump required data
```
./dumpsql.sh
```

* create ec2 instance
```
ansible-playbook create.yml
```

* start process
```
ansible-playbook -i ec2.py provision.yml
```

* destroy ec2 instance
```
ansible-playbook destroy.yml
```
