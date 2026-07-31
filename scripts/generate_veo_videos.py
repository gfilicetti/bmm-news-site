#!/usr/bin/env python3
"""
Veo Video Generator Script
Reads parameters from parameters.yaml, iterates through prompt .md files in prompts_dir,
and calls Google GenAI Veo API to generate sequential MP4 video files in output_dir.
"""

import os
import sys
import glob
import time
import yaml

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai
from google.genai import types

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "parameters.yaml")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    
    # Resolve directories relative to repository root
    repo_root = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
    prompts_dir = os.path.abspath(os.path.join(repo_root, config.get("prompts_dir", "scripts/prompts")))
    output_dir = os.path.abspath(os.path.join(repo_root, config.get("output_dir", "scripts/output")))
    output_prefix = config.get("output_prefix", "generated_video_")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .md files in prompts_dir
    prompt_files = sorted(glob.glob(os.path.join(prompts_dir, "*.md")))
    if not prompt_files:
        print(f"No .md prompt files found in {prompts_dir}")
        sys.exit(1)
        
    print(f"Found {len(prompt_files)} prompt file(s) in {prompts_dir}")
    print(f"Output directory: {output_dir}\n")
    
    # Initialize Google GenAI client using Application Default Credentials (ADC) via Vertex AI
    use_vertex = config.get("vertexai", True)
    project_id = config.get("project") or os.environ.get("GOOGLE_CLOUD_PROJECT") or "bmm-news-site"
    location = config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-central1"

    if use_vertex:
        print(f"Initializing Google GenAI Client with Application Default Credentials (ADC)...")
        print(f"    GCP Project: {project_id}")
        print(f"    GCP Region:  {location}\n")
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )
    else:
        client = genai.Client()

    model_name = config.get("model", "veo-2.0-generate-001")
    
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
            # Build Veo request config
            gen_config = types.GenerateVideosConfig(
                aspect_ratio=config.get("aspect_ratio", "16:9"),
                duration_seconds=config.get("duration_seconds", 8),
                person_generation=config.get("person_generation", "allow_adult"),
            )
            
            # Trigger video generation job using latest SDK source parameter
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
                generated_video = result.generated_videos[0]
                video_obj = generated_video.video
                video_bytes = getattr(video_obj, "video_bytes", None)

                # If video_bytes is not populated directly
                if not video_bytes:
                    if not use_vertex:
                        # Gemini Developer API uses client.files.download
                        client.files.download(file=video_obj)
                        video_bytes = getattr(video_obj, "video_bytes", None)
                    elif getattr(video_obj, "uri", None):
                        uri = video_obj.uri
                        if uri.startswith("http://") or uri.startswith("https://"):
                            import urllib.request
                            req = urllib.request.Request(uri)
                            with urllib.request.urlopen(req) as response:
                                video_bytes = response.read()
                        elif uri.startswith("gs://"):
                            try:
                                from google.cloud import storage
                                parts = uri[5:].split("/", 1)
                                bucket_name, blob_name = parts[0], parts[1]
                                storage_client = storage.Client(project=project_id)
                                bucket = storage_client.bucket(bucket_name)
                                blob = bucket.blob(blob_name)
                                video_bytes = blob.download_as_bytes()
                            except Exception as storage_err:
                                print(f"    Note: Failed downloading GCS URI {uri}: {storage_err}")

                if video_bytes:
                    with open(out_path, "wb") as f_out:
                        f_out.write(video_bytes)
                    print(f"    SUCCESS: Saved video to {out_path}\n")
                elif getattr(video_obj, "uri", None):
                    print(f"    SUCCESS: Video generated at URI: {video_obj.uri}\n")
                else:
                    print(f"    ERROR: Could not retrieve video content for {filename}\n")
            else:
                print(f"    ERROR: No generated video returned for {filename}\n")
                
        except Exception as e:
            print(f"    ERROR generating video for {filename}: {e}\n")

    print(f"All video generation tasks completed! Videos saved in: {output_dir}")

if __name__ == "__main__":
    main()
