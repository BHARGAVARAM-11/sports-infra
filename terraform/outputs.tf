output "s3_metadata_bucket" {
  value       = aws_s3_bucket.metadata.id
  description = "The ID of the metadata S3 bucket"
}

output "s3_videos_bucket" {
  value       = aws_s3_bucket.videos.id
  description = "The ID of the videos S3 bucket"
}

output "s3_logs_bucket" {
  value       = aws_s3_bucket.logs.id
  description = "The ID of the logs S3 bucket"
}

output "ec2_instance_id" {
  value       = aws_instance.pipeline_ec2.id
  description = "The ID of the EC2 instance"
}

output "ec2_public_ip" {
  value       = aws_instance.pipeline_ec2.public_ip
  description = "The public IP of the EC2 instance"
}

output "cloudwatch_rule_name" {
  value       = aws_cloudwatch_event_rule.daily_trigger.name
  description = "The name of the CloudWatch daily trigger"
}

