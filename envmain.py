import argparse
from logging import handlers
import logging
import sys
import webbrowser

import boto3
from botocore.exceptions import ClientError, WaiterError


def config():
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    handler = handlers.RotatingFileHandler(
            'debug.log',
            maxBytes=(1024*1024),
            backupCount=5
            )
    formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
 
def _create_cf_connection(args):
    # Connect to a cloudformation
    # Returns a cloudformation connection.
    # Throws exception if connect fails
    try:
        client = boto3.client('cloudformation')    
        return client
    
    except Exception:
        raise
    
def is_keypair_exist(args):
    try:
        client = boto3.client('ec2')
        return (client.describe_key_pairs(KeyNames=[args.ssh_key_pair]))
    except Exception:
        raise   
    

def create_stack(args):
    try:
        conn = _create_cf_connection(args)
        f = open("./a4tp7.json", "r")
        json_data = f.read()
        f.close()
        
        resp = conn.create_stack(StackName=args.stack_name,
            TemplateBody=json_data,
    #            template_url='https://s3.amazonaws.com/stcolb-default-bucket/a4tp7.json',
    #            template_body=json_data, 
            Parameters=[
                {
                    'ParameterKey' :'KeyName',
                    'ParameterValue' : args.ssh_key_pair
                }
            ],
            DisableRollback=False, 
            TimeoutInMinutes=5, 
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'MiniProjectWebServer'
                }
            ]
        )
        return resp 
    
    except Exception:
        raise


if __name__=='__main__':
    try:
        #initialize logging utility
        config();
        logger = logging.getLogger('app')
        
        #  parse the command line
        if len(sys.argv) < 3:
            print("Usage:")
            print('\tpython envmain.py --stack-name <name> --ssh-key-pair <ssh keypair>\n')
            print('Where:')
            print('\t<name> is the name you give to the stack that will be created.')
            print('\t<ssh keypair> is the name of the .pem file used for authorization.\n')
            print('Example:')
            print('\tpython envmain.py --stack-name a4tpstack --ssh-key-pair myec2keypair\n\n')
            exit(1)
            
        parser = argparse.ArgumentParser()
        parser.add_argument("--stack-name")
        parser.add_argument("--ssh-key-pair")
        args = parser.parse_args()

        logger.info('Provisioning environment for stack %s.' % args.stack_name)
        
        # validate the ssh-key-pair
        is_keypair_exist(args)
        
        
        #  create a new stack and wait until complete  
        resp = create_stack(args)
        client = _create_cf_connection(args)
        waiter = client.get_waiter('stack_create_complete')
        waiter.wait(StackName=args.stack_name)
        logger.info('Stack creation completed.')  
        
        # now get the output URL and open it
        cloudformation = boto3.resource('cloudformation')
        stackId = resp.get("StackId")
        stack = cloudformation.Stack(stackId)
        outputs = stack.outputs
        urlAddr = outputs[0]['OutputValue']
        logger.info('This is the URL: %s' % urlAddr)
        webbrowser.open(urlAddr, new=1, autoraise=True)
        exit(0)

    except ClientError as e:
#        if e.response['Error']['Code'] == 'AlreadyExistsException':
        logger.error(e.response['Error']['Message'])
        logger.error('Stack creation failed!')
        
    except WaiterError as we:
        logger.error(we)
        logger.error('Stack creation failed!')
        
        
 
        