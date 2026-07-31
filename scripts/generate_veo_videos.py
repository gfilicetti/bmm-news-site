#!/usr/bin/env python3
"""
Veo Video Generator Script (Vertex AI ADC Only)
Reads parameters from parameters.yaml, iterates through prompt .md files in prompts_dir,
and calls Google GenAI Veo API on Vertex AI using Application Default Credentials.
"""

import os
import sys
import glob
import time
import yaml
import urllib.request
from google import genai
from google.genai import types

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "parameters.yaml")
EXAMPLE_CONFIG_PATH = os.path.join(SCRIPT_DIR, "parameters.yaml.example")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        print(f"Please copy the example configuration file and set your GCP Project ID:")
        print(f"    cp scripts/parameters.yaml.example scripts/parameters.yaml\n")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_video_bytes(video_obj, out_path, project_id):
    """Extracts video bytes directly or downloads from Vertex AI output URI."""
    video_bytes = getattr(video_obj, "video_bytes", None)

    if not video_bytes and getattr(video_obj, "uri", None):
        uri = video_obj.uri
        if uri.startswith("http://") or uri.startswith("https://"):
            req = urllib.request.Request(uri)
            with urllib.request.urlopen(req) as response:
                video_bytes = response.read()
        elif uri.startswith("gs://"):
            try:
                from google.cloud import storage
                parts = uri[5:].split("/", 1)
                storage_client = storage.Client(project=project_id)
                bucket = storage_client.bucket(parts[0])
                blob = bucket.blob(parts[1])
                video_bytes = blob.download_as_bytes()
            except Exception as e:
                print(f"    Note: Failed downloading GCS URI {uri}: {e}")

    if video_bytes:
        with open(out_path, "wb") as f_out:
            f_out.write(video_bytes)
        print(f"    SUCCESS: Saved video to {out_path}\n")
    elif getattr(video_obj, "uri", None):
        print(f"    SUCCESS: Video generated at URI: {video_obj.uri}\n")
    else:
        print(f"    ERROR: Could not retrieve video bytes.\n")


def main():
    config = load_config()

    repo_root = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
    prompts_dir = os.path.abspath(os.path.join(repo_root, config.get("prompts_dir", "scripts/prompts")))
    output_dir = os.path.abspath(os.path.join(repo_root, config.get("output_dir", "scripts/output")))
    output_prefix = config.get("output_prefix", "generated_video_")

    os.makedirs(output_dir, exist_ok=True)

    prompt_files = sorted(glob.glob(os.path.join(prompts_dir, "*.md")))
    if not prompt_files:
        print(f"No .md prompt files found in {prompts_dir}")
        sys.exit(1)

    project_id = config.get("project") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location", "us-central1")

    if not project_id or project_id == "your-gcp-project-id":
        print("Error: Please specify a valid GCP project in scripts/parameters.yaml")
        sys.exit(1)

    print(f"Initializing Google GenAI Client (Vertex AI / ADC)...")
    print(f"    GCP Project: {project_id}")
    print(f"    GCP Region:  {location}")
    print(f"    Prompts Dir: {prompts_dir}")
    print(f"    Output Dir:  {output_dir}\n")

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )

    model_name = config.get("model", "veo-3.1-lite-generate-001")

    for idx, prompt_file in enumerate(prompt_files, start=1):
        filename = os.path.basename(prompt_file)
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()

        out_filename = f"{output_prefix}{idx:02d}.mp4"
        out_path = os.path.join(output_dir, out_filename)

        print(f"[{idx}/{len(prompt_files)}] Processing '{filename}'...")
        print(f"    Prompt: \"{prompt_text[:80]}...\"")
        print(f"    Target output: {out_filename}")

        try:
            gen_config = types.GenerateVideosConfig(
                aspect_ratio=config.get("aspect_ratio", "16:9"),
                duration_seconds=config.get("duration_seconds", 8),
                person_generation=config.get("person_generation", "allow_adult"),
            )

            operation = client.models.generate_videos(
                model=model_name,
                source=types.GenerateVideosSource(
                    prompt=prompt_text,
                ),
                config=gen_config,
            )

            print("    Waiting for Veo video generation to complete...")
            while not operation.done:
                time.sleep(10)
                operation = client.operations.get(operation)
                print(".", end="", flush=True)
            print()

            result = operation.result
            if result and result.generated_videos:
                save_video_bytes(result.generated_videos[0].video, out_path, project_id)
            else:
                print(f"    ERROR: No generated video returned for {filename}\n")

        except Exception as e:
            print(f"    ERROR generating video for {filename}: {e}\n")

    print(f"All video generation tasks completed! Videos saved in: {output_dir}")


if __name__ == "__main__":
    main()
