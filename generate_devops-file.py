import ollama
import yaml
import json

def ask_ollama(prompt, model="llama3"):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def prettify_output(content, file_type):
    try:
        if file_type.endswith((".yaml", ".yml")):
            return yaml.safe_dump(yaml.safe_load(content), sort_keys=False)
        elif file_type.endswith(".json"):
            return json.dumps(json.loads(content), indent=2)
    except Exception:
        pass
    return content

def get_prompt_for_task(task, description, extras):
    prompts = {
        "1": (
            "Dockerfile",
            f"""
Write a production-grade Dockerfile for a {extras.get('language')} application with the following description:

{description}

Use multi-stage builds, minimize image size, include .dockerignore recommendations, and expose necessary ports.
- Base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
- Follows Security Best Practices
- Seprate Phases for each
- Ask where infomation is needed
            """
        ),
        "2": (
            "buildspec.yml",
            f"""
Generate a CodeBuild buildspec.yml file for the application:

{description}

Include install, pre_build, build, and post_build phases, and follow best practices.
Include:
- Phases (install, pre_build, build, post_build)
- Environment variables
- Artifacts (if applicable)
- Ask where infomation is needed
- Follows Security Best Practices

            """
        ),
        "3": (
            "terraform.tf",
            f"""
Create a Terraform configuration to deploy this infrastructure:

Description: {description}

Type of infrastructure: {extras.get('infra_type')}

Include necessary components such as VPCs, IAM, ECS, EKS, or RDS based on the request.
- Provider block
- Resource block
- Variables
- Ask where infomation is needed
- Outputs
- Follows Security Best Practices
            """
        ),
        "4": (
            "cloudformation.yaml",
            f"""
Create a CloudFormation YAML template to provision infrastructure:

Description: {description}

Type of infrastructure: {extras.get('infra_type')}

Use best practices for modularity and security. Include IAM, networking, storage, etc.
- AWSTemplateFormatVersion
- Description
- Resources section
- Parameters and Outputs
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "5": (
            "ansible-playbook.yaml",
            f"""
Write an Ansible playbook to configure and deploy the following:

{description}

Include common roles like docker, firewall, users, nginx, etc.
- Hosts definition
- Tasks
- Handlers (if needed)
- Variables
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "6": (
            "k8s_deployment.yaml",
            f"""
Write a Kubernetes Deployment YAML for this app:

{description}

Use resource limits: {extras.get('resources')}
Include labels, probes, environment variables, and replicas.
- apiVersion
- kind
- metadata
- spec with replicas, template, containers, and labels
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "7": (
            "k8s_service.yaml",
            f"""
Write a Kubernetes Service YAML for the app described below:

{description}

Type of service: {extras.get('service_type')}
- apiVersion
- kind
- metadata
- spec with selector, type, and ports
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "8": (
            "k8s_ingress.yaml",
            f"""
Create a Kubernetes Ingress resource in YAML format for this app:

{description}

Ingress Controller: {extras.get('ingress_controller')}
Enable TLS, use path-based routing, and include annotations if needed.
- apiVersion
- kind
- metadata
- spec with rules and backend configuration
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "9": (
            "kyverno-policy.yaml",
            f"""
Generate a Kyverno policy to enforce pod security for this workload:

{description}

Restrict hostPath, enforce runAsNonRoot, drop all capabilities, and disallow privilege escalation.
- apiVersion
- kind
- metadata
- spec with validation rules
- Ask where infomation is needed
- Follows Security Best Practices
            """
        ),
        "10": (
            "helm_chart.yaml",
            f"""
Generate a basic Helm chart for this application:

{description}

Include Chart.yaml, values.yaml, templates/deployment.yaml using template syntax and best practices.
- Chart.yaml
- values.yaml
- templates/deployment.yaml
- templates/service.yaml
- Follows Security Best Practices
- Ask where infomation is needed
            """
        )
    }
    return prompts.get(task)

def main():
    tasks = {
        "1": "Dockerfile",
        "2": "BuildSpec (buildspec.yml)",
        "3": "Terraform",
        "4": "CloudFormation",
        "5": "Ansible Playbook",
        "6": "K8s Deployment",
        "7": "K8s Service",
        "8": "K8s Ingress",
        "9": "Kyverno Pod Security",
        "10": "Helm Chart"
    }

    print("📦 What would you like to generate? (Choose one task only)")
    for k, v in tasks.items():
        print(f"{k}. {v}")

    choice = input("Enter your choice (1-10): ").strip()
    if choice not in tasks:
        print("❌ Invalid choice.")
        return

    description = input("\n📝 Describe your application or infrastructure:\n").strip()
    extras = {}

    if choice == "1":
        extras["language"] = input("💬 What language is your app written in (e.g., Python, Node.js)? ").strip()
    if choice in ["3", "4"]:
        extras["infra_type"] = input("🌐 What kind of infrastructure do you want to create (e.g., ECS, EKS, EC2, RDS)? ").strip()
    if choice == "6":
        extras["resources"] = input("⚙️ Specify CPU/Memory limits (e.g., 200m CPU, 512Mi memory): ").strip()
    if choice == "7":
        extras["service_type"] = input("🔌 What type of K8s Service? (ClusterIP, NodePort, LoadBalancer): ").strip()
    if choice == "8":
        extras["ingress_controller"] = input("🌍 Which Ingress Controller are you using? (nginx, AWS ALB, Azure, etc.): ").strip()

    # Ask for desired output format
    output_format = input("📁 Output format? (yaml/json): ").strip().lower()
    if output_format not in ["yaml", "json"]:
        print("⚠️ Invalid format. Defaulting to YAML.")
        output_format = "yaml"

    filename, prompt = get_prompt_for_task(choice, description, extras)
    if not prompt:
        print("⚠️ Failed to build prompt.")
        return

    print(f"\n🧠 Generating {tasks[choice]}...")
    result = ask_ollama(prompt)

    # Convert filename extension based on format
    if not filename.lower().endswith("dockerfile"):  # Dockerfile has no extension
        filename = filename.rsplit(".", 1)[0] + (".json" if output_format == "json" else ".yaml")

    # Format the output
    if output_format == "json":
        try:
            parsed = yaml.safe_load(result)
            formatted = json.dumps(parsed, indent=2)
        except Exception:
            print("⚠️ Failed to parse YAML. Outputting raw response.")
            formatted = result
    else:
        formatted = prettify_output(result, filename)

    # Save file
    with open(filename, "w") as f:
        f.write(formatted)

    print(f"\n✅ {tasks[choice]} saved to {filename}")
    print(f"\n📄 Full Output:\n{formatted}")


if __name__ == "__main__":
    main()
