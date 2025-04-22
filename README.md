# 🛠️ DevOps Generator CLI (with Ollama AI)

This is a Python-based CLI tool that leverages [Ollama](https://ollama.com) models (like LLaMA3, Mistral, etc.) running locally to auto-generate DevOps infrastructure files such as:

- Dockerfile (with best practices)
- AWS CodeBuild `buildspec.yml`
- Terraform configurations
- CloudFormation templates
- Ansible playbooks
- Kubernetes YAMLs (Deployment, Service, Ingress, etc.)
- Kyverno security policies
- Helm charts

---

## 🚀 Features

- Uses **locally running Ollama models** via the `ollama` Python package
- Prompts for essential input only
- Auto-formats YAML/JSON output
- Supports one task per run (ensures focused results)
- Follows DevOps best practices by default

---

## 📦 Requirements

- Python 3.7+
- Local [Ollama](https://ollama.com) instance running (e.g., `ollama run llama3`)
- Required Python packages:

```bash
pip install -r requirements.txt
requirements.txt

nginx
Copy
Edit
ollama
PyYAML
🧑‍💻 Usage
Run the script:

bash
Copy
Edit
python devops_gen.py
You’ll be prompted to choose one of the following:

markdown
Copy
Edit
1. Dockerfile
2. BuildSpec (buildspec.yml)
3. Terraform
4. CloudFormation
5. Ansible Playbook
6. K8s Deployment
7. K8s Service
8. K8s Ingress
9. Kyverno Pod Security
10. Helm Chart
Then answer task-specific questions like:

💬 Language of your app (for Dockerfile)

🧪 How the app runs (e.g., Flask with Gunicorn, Express server)

⚙️ Resource limits (for Kubernetes)

🌐 Infrastructure type (e.g., EKS, EC2, RDS)

🌍 Ingress controller (e.g., NGINX, AWS ALB)

📁 Output
Generated files are saved directly to the current directory, e.g.:

Dockerfile

terraform.tf

k8s_deployment.yaml

cloudformation.yaml

helm_chart.yaml

Output is also prettified automatically if it's YAML or JSON.

🔒 Security
All generation happens locally. No data is sent over the internet — you're using your own locally running Ollama model.

🧠 Ideas for Expansion
Add support for multiple files per run (with --all)

Convert to devgen CLI tool with argparse

Include option to preview without saving

Add language-specific Docker templates

Export Helm charts as a folder structure