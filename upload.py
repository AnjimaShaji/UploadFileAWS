provider "aws" {
  region = "us-east-1" # Change to your desired region
}

# S3 Bucket for Data Upload
resource "aws_s3_bucket" "data_bucket" {
  bucket = "your-data-bucket-name"
  acl    = "private"
}

# Lambda Function for Triggering the Python Script
resource "aws_lambda_function" "data_processing_lambda" {
  function_name = "data-processing-lambda"
  handler      = "lambda.handler"
  runtime      = "python3.8"
  role         = aws_iam_role.lambda_role.arn
}

# IAM Role for Lambda Function
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Trigger Lambda on S3 Object Creation
resource "aws_lambda_permission" "s3_trigger_permission" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_processing_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.data_bucket.arn
}

# Visualization Tool (QuickSight)
resource "aws_quicksight_group" "visualization_group" {
  group_name = "visualization-group"
}

resource "aws_quicksight_user" "visualization_user" {
  user_name         = "visualization-user"
  email             = "user@example.com"
  identity_type     = "IAM"
  aws_account_id    = "your-aws-account-id"
  namespace         = "default"
  group_membership  = [aws_quicksight_group.visualization_group.arn]
}

# Define Data Pipeline and Dependencies
# Implement your logic here to orchestrate the entire pipeline

# Example: S3 Event Notification
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.data_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.data_processing_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
}
