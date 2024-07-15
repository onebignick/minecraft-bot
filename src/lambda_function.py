import json
import os

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import boto3

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
EC2_INSTANCE_ID = os.environ.get("EC2_INSTANCE_ID")

class DiscordEvent():
    def handle_event(self, event_type):
        try:
            handler = getattr(self, f"handle_{event_type}")
        except AttributeError:
            handler = self.handle_unsupported()
        response = handler()
        return response
    
    def handle_start_server(self):
        ec2_client = boto3.client("ec2")
        response = ec2_client.start_instances(
            InstanceIds=[
                EC2_INSTANCE_ID,
            ],
            DryRun=False
        )
        print(response)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "type": 4,
                "data": {
                    "content": "Starting server... It's gregging time.",
                }
            })
        }


    def handle_reboot_server(self):
        ec2_client = boto3.client("ec2")
        response = ec2_client.reboot_instances(
            InstanceIds=[
                EC2_INSTANCE_ID,
            ],
            DryRun=False
        )
        print(response)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "type": 4,
                "data": {
                    "content": "Yo what the sigma? Rebooting real quick",
                }
            })
        }


    def handle_stop_server(self):
        ec2_client = boto3.client("ec2")
        response = ec2_client.reboot_instances(
            InstanceIds=[
                EC2_INSTANCE_ID,
            ],
            DryRun=False
        )
        print(response)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "type": 4,
                "data": {
                    "content": "Stopping server!",
                }
            })
        }


    def handle_unsupported(self):
        return {
            "statusCode": 400,
            "body": json.dumps("Unsupported request type")
        }


def lambda_handler(event, context):
    print(event)
    try:
        signature = event["headers"]["x-signature-ed25519"]
        timestamp = event["headers"]["x-signature-timestamp"]

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        message = timestamp + event["body"]

        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {
                "statusCode": 401,
                "body": json.dumps("invalid request signature")
            }
        
        body = json.loads(event["body"])
        discord_event_type = body["type"]
        discord_event_handler = DiscordEvent()
        print(body)
        match discord_event_type:
            case 1:
                return {"statusCode": 200, "body": json.dumps({"type": 1})}
            case 2:
                return discord_event_handler.handle_event(body["data"]["name"]);
            case _:
                return {"statusCode": 500, "body": json.dumps("Unsupported type")}

    except Exception as e:
        print(e)
        raise e
