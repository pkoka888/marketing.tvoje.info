# Image Generation LLM Resource Requirements

This document provides comprehensive resource requirements for popular image generation models including SDXL, Stable Diffusion 1.5, FLUX, and ComfyUI.

## Table of Contents
1. VRAM Requirements
2. RAM Requirements
3. CPU vs GPU Performance
4. Comparison Table
5. Recommendations

---

## VRAM Requirements

### Stable Diffusion XL (SDXL)

| Use Case | Minimum VRAM | Recommended VRAM |
|----------|--------------|------------------|
| Base model only (1024x1024) | 6 GB | 8 GB |
| Base + Refiner | 12 GB | 16 GB |
| With LoRAs + ControlNet | 12 GB | 16+ GB |
| Training/Fine-tuning | 24 GB | 24+ GB |

### Stable Diffusion 1.5

| Use Case | Minimum VRAM | Recommended VRAM |
|----------|--------------|------------------|
| txt2img (512x512, batch 1) | 4 GB | 6 GB |
| With optimizations (attention slicing) | 2 GB | 4 GB |
| img2img + ControlNet | 6 GB | 8 GB |
| Training/Fine-tuning | 12 GB | 16 GB |

### FLUX (Black Forest Labs)

| Model Variant | Minimum VRAM | Recommended VRAM |
|---------------|--------------|------------------|
| FLUX.1 Dev (FP16) | 24 GB | 24 GB |
| FLUX.1 Dev (FP8) | 16 GB | 24 GB |
| FLUX.1 Schnell (FP8) | 12 GB | 16 GB |
| FLUX.1 Dev (NF4/GGUF) | 8 GB | 12 GB |
| Training LoRA | 24 GB | 24+ GB |

### ComfyUI

ComfyUI is a UI framework - VRAM requirements depend on the models loaded.

| Configuration | Minimum VRAM | Recommended VRAM |
|--------------|--------------|------------------|
| Basic workflows (SD 1.5) | 4 GB | 8 GB |
| SDXL workflows | 8 GB | 16 GB |
| FLUX workflows | 12 GB | 24 GB |
| Complex multi-model workflows | 16 GB | 24+ GB |

---

## RAM Requirements

| Model | Minimum RAM | Recommended RAM |
|-------|-------------|-----------------|
| SD 1.5 | 8 GB | 16 GB |
| SDXL | 16 GB | 32 GB |
| FLUX | 16 GB | 32 GB |
| ComfyUI | 8 GB | 16 GB |

Note: System RAM is used for the operating system, Python interpreter, model loading/swapping, and VRAM offloading.

---

## CPU vs GPU Performance

### Performance Comparison (approximate, on RTX 4090)

| Metric | GPU (RTX 4090) | CPU (Modern) | Speedup |
|--------|----------------|--------------|---------|
| SD 1.5 (512x512) | 20 it/s | 0.5-1 it/s | 20-40x |
| SDXL (1024x1024) | 10 it/s | 0.2-0.5 it/s | 20-50x |
| FLUX (1024x1024) | 5 it/s | 0.1-0.2 it/s | 25-50x |

### When CPU Can Be Used
- Testing/Debugging workflows
- Low VRAM systems with CPU offloading
- Battery/portable devices
- Very light workflows with SD 1.5

### GPU Recommendations

| Use Case | Recommended GPU |
|----------|------------------|
| Casual/SD 1.5 only | RTX 3060 12GB, RTX 4060 Ti |
| SDXL + some FLUX | RTX 4070 Super, RTX 4080 |
| FLUX + SDXL | RTX 4090, RTX 4080 Super |
| Professional/All models | RTX 4090, A100 |

---

## Comparison Table

| Model/Tool | Parameters | Min VRAM | Rec VRAM | Min RAM | Generation Speed | Best For |
|------------|------------|----------|----------|---------|------------------|----------|
| SD 1.5 | 860M | 4 GB | 8 GB | 8 GB | Fast | Legacy, low-end GPU |
| SDXL | 6.6B | 8 GB | 16 GB | 16 GB | Medium | General purpose |
| FLUX Dev | 12B | 24 GB | 24 GB | 32 GB | Medium | SOTA quality |
| FLUX Schnell | 12B | 12 GB | 16 GB | 16 GB | Fast | Speed |
| FLUX NF4 | 12B (4-bit) | 8 GB | 12 GB | 16 GB | Medium | Low VRAM |
| ComfyUI | N/A | 4 GB | 16 GB | 8 GB | Varies | Workflow automation |

Speed measured on RTX 4090, 1024x1024, 20 steps

---

## Recommendations

### Budget-Conscious (Under USD 500)
- GPU: RTX 3060 12GB or RTX 4060 Ti 16GB
- Models: SD 1.5, SDXL with optimizations

### Mid-Range (USD 500-1000)
- GPU: RTX 4070 Super or RTX 4080
- Models: SDXL, FLUX Schnell/FP8

### High-End (USD 1500+)
- GPU: RTX 4090 24GB
- Models: All including FLUX Dev

### Minimum to Run Anything
- VRAM: 8 GB
- RAM: 16 GB
- Model: SDXL or FLUX with quantization

---

## Sources
- ComfyUI Official Documentation
- Reddit r/StableDiffusion
- Hugging Face model discussions
- NVIDIA Blog
- Community benchmarks

Last Updated: January 2025
