# a4tp
Mini Project - Automatic for the People
---------------------------------------

This project will create an aws stack that has one ec2 instance.  The EC2 instance has an 
Apache WebServer installed on it.  There is also a default html page that is installed.  The 
script that accomplishes all this is written in Python.

One-Time Setup Procedures
-------------------------

The following items must be completed before executing the python script from your workstation.

1.  Create an AWS account if you don't have one already  
2.  Create an AWS user in that account and generate IAM Access Keys (AWS Access Key ID and AWS Secret Access Key)  
3.  install the AWS CLI package and run the 'aws configure' CLI utility  
4.  install Python 3.4 on your workstation  
5.  install boto3 on your workstation  
6.  generate an ssh-key-pair file (this is a required parameter when running the provisioning script)  

If you need additional information about setting up AWS CLI, please look to the Amazon Web
Services documentation for complete details.

How to Provision the 'Automatic for the People' Stack (Windows)
---------------------------------------------------------------
1. Download this repo  
2. Open a DOS Box and navigate to the folder where code was downloaded
3. Run the provisioner script:  
    Usage:  
    python envmain.py --stack-name ***name*** --ssh-key-pair ***sshkeypair***  
  
    Where:  
    ***name*** is the name you give to the stack that will be created.  
    ***sshkeypair*** is the name of the .pem file used for authorization.  
  
    Example:  
    python envmain.py --stack-name a4tpstack --ssh-key-pair myec2keypair  
		
		
