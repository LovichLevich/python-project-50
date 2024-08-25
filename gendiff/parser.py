import json  # type: ignore
import yaml  # type: ignore


def parse(data: str, format: str) -> dict:
    if format == "json":
        return json.loads(data)
    elif format == "yaml" or format == "yml":
        return yaml.safe_load(data)
    else:
        raise ValueError(f"Unsupported file format: {format}")
