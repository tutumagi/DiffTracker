import os
import yaml

# 读取yaml文件配置
yaml_path = os.path.join(os.path.dirname(__file__), "env.yaml")
with open(yaml_path, "r") as file:
    config = yaml.safe_load(file)

# Slack 相关配置
SLACK_TOKEN = config.get("slack", {}).get("api_token", "")
