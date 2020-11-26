#!/usr/bin/env python3
import argparse
import sys

import boto3

client = boto3.client('route53')


def get_hosted_zone_id_and_name():
    response = client.list_hosted_zones(MaxItems='1')
    return response['HostedZones'][0]['Id'].split('/')[-1], response['HostedZones'][0]['Name'][:-1]


def run(svc, cluster):
    zone_id, zone_name = get_hosted_zone_id_and_name()

    try:
        response = client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': "{}.{}".format(svc, zone_name),
                            'Type': 'CNAME',
                            'TTL': 0,
                            'ResourceRecords': [{'Value': "{}-{}".format(svc, cluster)}]
                        }

                    }
                ]
            }
        )
        print(response)
        exit(0)
    except client.exceptions.InvalidChangeBatch as e:
        print("Error:", e.response['Error']['Message'].lstrip('[').rstrip(']'), file=sys.stderr)
        print("It is possible that the record already exists as an A record"
              " so it can not be changed to CNAME. Check Route53",
              file=sys.stderr)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--service', required=True,
                        help='name of service, example: my-service')
    parser.add_argument('-c', '--cluster', required=True,
                        help='name of the cluster, example: blue/green')
    args = parser.parse_args()
    run(args.service, args.cluster)
