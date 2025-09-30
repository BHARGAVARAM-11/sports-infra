*Sports Highlights Pipeline*

**overview**

This project fetches basketball highlights from RapidAPI, stores the metadata in S3, downloads the highlight videos, and uploads them to S3. The project is packaged in a Docker container for easy deployment, and the infrastructure is managed using Terraform.

**Features**

Fetch highlight metadata from RapidAPI for a specific date and league.
Save metadata as JSON to an S3 bucket.
Download the first video from the highlights and upload it to S3.
Fully containerized using Docker.
Supports .env configuration for easy environment management.
Infrastructure managed with Terraform (S3 buckets, IAM roles, etc.).

**Prerequisites**
Python 3.11+
Docker
AWS account with access keys for S3
RapidAPI account with API key for sports highlights API

**Environment Variables**
Create a .env file in the project root with the following variables:

```env
API_URL=https://sport-highlights-api.p.rapidapi.com/basketball/highlights
RAPIDAPI_HOST=sport-highlights-api.p.rapidapi.com
RAPIDAPI_KEY=your_rapidapi_key_here
DATE=2023-08-30
LEAGUE_NAME=NCAA
LIMIT=10
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
S3_BUCKET_NAME=sports-highlights-bucket
```

*Terraform installation & setup*
The terraform/ folder contains the infrastructure as code for provisioning AWS resources

```env
**#Initialize Terraform**
cd terraform
terraform init

# Preview resources
terraform plan

# Apply configuration
terraform apply
```
**Project Structure**
sports-infra/
├── app/                 # Application code + Docker build context
│   ├── python.py        # Main pipeline script
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Docker container
├── project/             # Additional project configs
├── terraform/           # Terraform IaC for AWS resources
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── provider.tf
│   └── terraform.tfstate
└── .env                 # Environment variables



