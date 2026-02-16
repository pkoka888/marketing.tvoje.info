import os
import sys
import argparse
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_with_openai(prompt, output_file):
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found.")
            return False

        client = OpenAI(api_key=api_key)

        print(f"Generating image with DALL-E 3: {prompt[:50]}...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url"
        )

        image_url = response.data[0].url
        print(f"Image generated! Downloading from {image_url[:50]}...")

        img_data = requests.get(image_url).content
        with open(output_file, 'wb') as handler:
            handler.write(img_data)
        print(f"Saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating with OpenAI: {e}")
        return False

def generate_with_nvidia(prompt, output_file):
    try:
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            print("Error: NVIDIA_API_KEY not found.")
            return False

        invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "NONE",
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        print(f"Generating image with NVIDIA SDXL: {prompt[:50]}...")
        response = requests.post(invoke_url, headers=headers, json=payload)

        response.raise_for_status()
        body = response.json()

        # NVIDIA returns artifacts list with base64
        if "artifacts" in body and len(body["artifacts"]) > 0:
            b64_data = body["artifacts"][0]["base64"]
            img_data = base64.b64decode(b64_data)

            with open(output_file, 'wb') as handler:
                handler.write(img_data)
            print(f"Saved to {output_file}")
            return True
        else:
            print(f"Unexpected response format from NVIDIA: {body}")
            return False

    except Exception as e:
        print(f"Error generating with NVIDIA: {e}")
        if hasattr(e, 'response') and e.response:
             print(f"Response content: {e.response.text}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate images using AI providers')
    parser.add_argument('--prompt', required=True, help='Image generation prompt')
    parser.add_argument('--output', required=True, help='Output filename (e.g. image.png)')
    parser.add_argument('--provider', default='nvidia', choices=['openai', 'gemini', 'nvidia'], help='AI Provider')

    args = parser.parse_args()

    success = False
    if args.provider == 'openai':
        success = generate_with_openai(args.prompt, args.output)
    elif args.provider == 'nvidia':
        success = generate_with_nvidia(args.prompt, args.output)
    elif args.provider == 'gemini':
         print("Gemini unavailable due to 503 errors and script limitations.")
         success = False

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
