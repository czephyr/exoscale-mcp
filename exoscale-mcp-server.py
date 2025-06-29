from typing import Any, Dict, List
import os
from mcp.server.fastmcp import FastMCP
from exoscale.api.v2 import Client

# Initialize FastMCP server
mcp = FastMCP("exoscale-portal")

EXO_KEY_NAME = os.getenv("EXO_KEY_NAME", "EXO35...")
EXO_KEY_SECRET = os.getenv("EXO_KEY_SECRET", "etzR-...")

def format_vm_details(data: Dict[str, List[Dict[str, Any]]], client) -> str:
    """
    Formats a dictionary containing a list of VM instances into a human-readable string,
    showing ID, Name, Template ID, Instance Type ID, and Public IP.

    Args:
        data: A dictionary expected to have an 'instances' key,
              where its value is a list of dictionaries, each representing a VM.

    Returns:
        A formatted string listing the details of each VM.
        Returns "No VM instances found." if the input is empty or malformed.
    """
    instances = data.get('instances')
    if not instances:
        return "No VM instances found."

    formatted_output = []
    for vm in instances:
        vm_id = vm.get('id', 'N/A')
        name = vm.get('name', 'N/A')
        template_id = client.get_template(id=vm.get('template', {}).get('id', 'N/A'))["name"]
        instance_type_id = f"{client.get_instance_type(id=vm.get('instance-type', {}).get('id', 'N/A'))["family"]} {client.get_instance_type(id=vm.get('instance-type', {}).get('id', 'N/A'))["size"]}"
        public_ip = vm.get('public-ip', 'N/A')
        state = vm.get('state', 'Unknown')
        disk_size = vm.get('disk_size',0)
        formatted_output.append(f"""
VM ID: {vm_id}
Name: {name}
State: {state}
Template: {template_id}
Instance Type: {instance_type_id}
Public IP: {public_ip}
Disk Size: {disk_size} GB
--------------------""")

    return "\n".join(formatted_output).strip()


@mcp.tool()
async def get_running_vms() -> str:
    """Get the VMs currently running on the Exoscale account.
    """
    c = Client(EXO_KEY_NAME, EXO_KEY_SECRET)

    return format_vm_details(c.list_instances(),c)


@mcp.tool()
async def create_vm(vm_name: str, disk_size: int) -> str:
    """Create a VM on the Exoscale account.

    Args:
        vm_name: the name of the new vm
        disk_size: the size of the disk in GB of the new vm
    """
    c = Client(EXO_KEY_NAME, EXO_KEY_SECRET)

    hardcoded_instance_type = c.get_instance_type(id="71004023-bb72-4a97-b1e9-bc66dfce9470")
    hardcoded_instance_template = c.get_template(id="cd6c18eb-1cc6-471a-ae9b-8a8f0e7ce507")
    response = c.create_instance(name=vm_name,instance_type=hardcoded_instance_type,template=hardcoded_instance_template, disk_size=disk_size)
    return response["state"]

@mcp.tool()
async def delete_vm_by_name(vm_name: str) -> str:
    """Delete a vm on the Exoscale account by its name.
    """
    c = Client(EXO_KEY_NAME, EXO_KEY_SECRET)

    response = c.list_instances()
    
    response = c.list_instances()
    for vm in response['instances']:
        if vm.get('name') == vm_name:
            answer = c.delete_instance(id=vm.get('id'))
            return answer["state"]
    return "VM not found"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')