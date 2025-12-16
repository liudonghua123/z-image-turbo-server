# Z-Image-Turbo Server

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-available-green.svg)

A high-performance, OpenAI-compatible AI image generation API server using the [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) model. Built with FastAPI and optimized for GPU inference.

## ✨ Features

- **High Speed**: Leverages Z-Image-Turbo for efficient single-stream diffusion generation.
- **OpenAI Compatible**: Drop-in replacement for OpenAI's `/v1/images/generations` endpoint.
- **Production Ready**: Containerized with Docker, inclusive of multi-stage builds and best practices.
- **Modern Tooling**: Built using `uv` for fast and reliable dependency management.
- **Configurable**: Easy configuration via `.env` files.

## 🚀 Quick Start

### Prerequisites

- NVIDIA GPU with CUDA drivers (required for `bfloat16` and reasonable generation speed).
- Docker and Docker Compose (recommended).
- Python 3.10+ (if running locally).

### 🐳 Running with Docker

1.  **Build the Image**
    ```bash
    docker build -t z-image-turbo-server .
    ```

2.  **Run the Container**
    Ensure you pass the GPU flags.
    ```bash
    docker run --gpus all -p 8000:8000 z-image-turbo-server
    ```

3.  **Test the API**
    ```bash
    curl http://localhost:8000/v1/images/generations \
      -H "Content-Type: application/json" \
      -d '{
        "prompt": "A cyberpunk city in the rain, neon lights",
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
      }'
    ```

### 🛠️ Local Development

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/z-image-turbo-server.git
    cd z-image-turbo-server
    ```

2.  **Install Dependencies**
    We use [uv](https://github.com/astral-sh/uv) for dependency management.
    ```bash
    pip install uv
    uv sync
    # OR using pip directly
    pip install -r pyproject.toml
    ```

3.  **Run the Server**
    ```bash
    uvicorn app.main:app --reload
    ```

## ⚙️ Configuration

Create a `.env` file in the root directory to override defaults:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `MODEL_ID` | `Tongyi-MAI/Z-Image-Turbo` | Hugging Face model ID |
| `DEVICE` | `cuda` | Device to run on (`cuda` or `cpu`) |
| `DTYPE` | `bfloat16` | Precision (`bfloat16` or `float16`) |

Example `.env`:
```env
MODEL_ID=Tongyi-MAI/Z-Image-Turbo
DEVICE=cuda
DTYPE=bfloat16
```

## 📡 API Reference

### Generate Image
`POST /v1/images/generations`

Compatible with OpenAI [Create Image API](https://platform.openai.com/docs/api-reference/images/create).

**Request Body:**
- `prompt` (str): A text description of the desired image.
- `n` (int, default=1): Number of images to generate (Currently processes sequentially).
- `size` (str, default="1024x1024"): Size of the generated image.
- `response_format` (str, default="url"): Format of the response ("url" or "b64_json").

## 🔄 CI/CD

This project includes a GitHub Action workflow for manual releases.
1. Go to **Actions** tab in GitHub.
2. Select **Build and Push Docker Image**.
3. Click **Run workflow**.
4. Enter the semantic version (e.g., `1.0.0`).

This will build the Docker image, push it to your configured registry, and create a GitHub Release.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) for the amazing model.
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [Diffusers](https://github.com/huggingface/diffusers) for the diffusion pipeline.
