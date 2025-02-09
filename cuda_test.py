import torch
print(torch.cuda.is_available())  # True なら CUDA 使用可能
print(torch.cuda.device_count())  # GPU の数
print(torch.cuda.get_device_name(0))  # 0 番目の GPU の名前