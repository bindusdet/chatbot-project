output "cluster_id" {
  value = aws_eks_cluster.bindu.id
}

output "node_group_id" {
  value = aws_eks_node_group.bindu.id
}

output "vpc_id" {
  value = aws_vpc.bindu_vpc.id
}

output "subnet_id" {
  value = aws_subnet.bindu_subnet[*].id
}