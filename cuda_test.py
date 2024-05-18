import torch
print(torch.__version__)
print(f"Cuda available: {torch.cuda.is_available()}")
print(f"Cuda devices count: {torch.cuda.device_count()}")
