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
    
    # Initialize Google GenAI client
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
            
            # Trigger video generation job
            operation = client.models.generate_videos(
                model=model_name,
                prompt=prompt_text,
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
                # Download/save video bytes
                client.files.download(file=generated_video.video)
                with open(out_path, "wb") as f_out:
                    f_out.write(generated_video.video.video_bytes)
                print(f"    SUCCESS: Saved video to {out_path}\n")
            else:
                print(f"    ERROR: No generated video returned for {filename}\n")
                
        except Exception as e:
            print(f"    ERROR generating video for {filename}: {e}\n")

    print(f"All video generation tasks completed! Videos saved in: {output_dir}")

if __name__ == "__main__":
    main()
