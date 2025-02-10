import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)  # изменено на 1 канал
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 10)  # 10 классов для цифр MNIST

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
 
model = SimpleCNN()
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()    
# print(4e3 == 4 * 10^3)
transform = transforms.Compose([
    transforms.Resize((32, 32)),  # размер до 32
    transforms.Grayscale(),
    transforms.RandomInvert(p=1),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

image_path = 'images.png'
image = Image.open(image_path).convert('L') 

# Применение преобразований
from helpers import plot
image = transform(image)
plot(image, cmap = 'gray')
plt.show()
image = image.unsqueeze(0)  

# Предсказание
with torch.no_grad():
    output = model(image)
    
    
    possibol, predicted = torch.max(output.data, 1)
    predicted_class = predicted.item()

print(predicted_class)
print(possibol%100)
    

plt.imshow(Image.open(image_path), cmap='gray')
plt.title(f'Predicted class: {predicted_class}')
plt.show()
