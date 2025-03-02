import torch
print(torch.cuda.is_available())  # Debería devolver True si CUDA está disponible
print(torch.cuda.current_device())  # Debería devolver el índice de la GPU
print(torch.cuda.get_device_name(0))  # Debería devolver el nombre de la GPU, como "NVIDIA GeForce GTX 1050"
print(torch.cuda.memory_allocated())