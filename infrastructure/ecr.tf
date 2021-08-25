resource "aws_ecr_repository" "repo" {
  name                 = "${local.prefix}-censo-escolar-extration-job"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}