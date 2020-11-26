# Route 53 Blue/Green Switch

## What it is

You have a service called "svc".

You have two EKS clusters, called "blue" and "green".

You deploy it in two different EKS clusters with different route53 names for blue/green deployment purpose, in the format of "{{ svc_name }}-{{ cluster_name }}.{{ zone_name}}", like:

- svc-blue.example.com
- svc-green.example.com

But you want the user to be blue/green agnostic, so you want the user to use:
svc.example.com to access the service.

You need a CNAME / Alias Record in Route53 to point "svc.example.com" to either "svc-blue.example.com` or `svc-green.example.com`, and you might need to do the switch from blue to green or vice versa from time to time. 

This tool is designed to upcert the route53 record for you to achieve blue/green switch.

## How to run

```
pip3 install -r requirements.txt 
```

Setup AWS access key ID / secret.

## Run

```shell script
$ chmod +x ./r53bgs.py 
$ ./r53bgs.py          
usage: r53bgs.py [-h] -s SERVICE -c CLUSTER
r53bgs.py: error: the following arguments are required: -s/--service, -c/--cluster
$ ./r53bgs.py -h
usage: r53bgs.py [-h] -s SERVICE -c CLUSTER

optional arguments:
  -h, --help            show this help message and exit
  -s SERVICE, --service SERVICE
                        name of service, example: my-service
  -c CLUSTER, --cluster CLUSTER
                        name of the cluster, example: blue/green

$ ./r53bgs.py -s svc -c blue

$ ./r53bgs.py --service svc --cluster green
```

## Note

This is supposed to be a temporary fast work around.
