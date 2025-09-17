"""
Kubernetes helper utilities for testing
"""
import subprocess
import json
from typing import Dict, List, Optional


class K8sHelper:
    """Helper class for Kubernetes operations during testing"""
    
    def __init__(self):
        self.context = "kind-nexus-cluster"
    
    def run_kubectl(self, command: str) -> subprocess.CompletedProcess:
        """Run kubectl command"""
        full_command = f"kubectl --context={self.context} {command}"
        return subprocess.run(
            full_command.split(),
            capture_output=True,
            text=True,
            check=False
        )
    
    def get_pods(self, namespace: str = None) -> List[Dict]:
        """Get pods from Kubernetes"""
        cmd = "get pods -o json"
        if namespace:
            cmd += f" -n {namespace}"
        
        result = self.run_kubectl(cmd)
        if result.returncode != 0:
            return []
        
        data = json.loads(result.stdout)
        return data.get('items', [])
    
    def get_services(self, namespace: str = None) -> List[Dict]:
        """Get services from Kubernetes"""
        cmd = "get services -o json"
        if namespace:
            cmd += f" -n {namespace}"
        
        result = self.run_kubectl(cmd)
        if result.returncode != 0:
            return []
        
        data = json.loads(result.stdout)
        return data.get('items', [])
    
    def is_pod_ready(self, pod_name: str, namespace: str) -> bool:
        """Check if a pod is ready"""
        pods = self.get_pods(namespace)
        for pod in pods:
            if pod['metadata']['name'] == pod_name:
                conditions = pod.get('status', {}).get('conditions', [])
                for condition in conditions:
                    if condition['type'] == 'Ready':
                        return condition['status'] == 'True'
        return False
    
    def get_pod_logs(self, pod_name: str, namespace: str, lines: int = 50) -> str:
        """Get pod logs"""
        result = self.run_kubectl(f"logs {pod_name} -n {namespace} --tail={lines}")
        return result.stdout if result.returncode == 0 else ""
    
    def port_forward(self, service: str, namespace: str, local_port: int, remote_port: int) -> subprocess.Popen:
        """Start port forwarding"""
        cmd = f"port-forward -n {namespace} svc/{service} {local_port}:{remote_port}"
        return subprocess.Popen(
            f"kubectl --context={self.context} {cmd}".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    def get_cluster_info(self) -> Dict:
        """Get cluster information"""
        result = self.run_kubectl("cluster-info")
        return {
            "status": "running" if result.returncode == 0 else "error",
            "output": result.stdout
        }
