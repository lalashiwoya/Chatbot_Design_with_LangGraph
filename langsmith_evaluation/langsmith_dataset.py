from typing import List, Tuple
from api.pydantic_model import UserSettings
from utils import read_configs_from_toml 
import pandas as pd

# config_path = "langsmith_evaluation/config.toml"
# configs = read_configs_from_toml(config_path)

def create_greeting_chat_history() -> List[dict]:
    return [{"input": "Hi", "output": "Hi, what can I help you?"}]

def create_sample_user_settings(configs) -> UserSettings:
    settings = UserSettings(llm_model_name=configs["agent"]["model_name"])
    return settings

def create_greeting_chat_history() -> List[dict]:
    return [{"input": "Hi", "output": "Hi, what can I help you?"}]

def create_sample_topics(topics: List[str] = ["Large Language Models (LLM) finetuning", "Explainable AI"]) -> str:
    return "\n".join(topics)

def create_langsmith_inputs_outputs(path: str) -> Tuple[List[dict], List[dict]]:
    df = pd.read_csv(path)
    chat_history = create_greeting_chat_history()
    inputs = []
    outputs = []
    for i in range(len(df)):
        question = df["questions"][i]
        reference = df["answers"][i]
        inputs.append({"question": question,
                    "chat_history": chat_history})
        outputs.append({"reference": reference})
    return inputs, outputs

def create_langsmith_dataset(client, dataset_name:str, dataset_description: str, csv_path: str):
    if client.has_dataset(dataset_name=dataset_name):
        print(f"Datast {dataset_name} already exists")
    else:
        dataset = client.create_dataset(dataset_name, description=dataset_description)
        inputs, outputs = create_langsmith_inputs_outputs(csv_path)
        client.create_examples(inputs=inputs, outputs=outputs,
                            dataset_id=dataset.id)
        print(f"Datast {dataset_name} is created now!")


 