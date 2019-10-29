# -*- coding: utf-8 -*-
"""Choejaegun

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CvKWiTXYTSw4fp5tilhpQzEfyAVABQq5

## 1) Gradient descent

**Gradient descent**

함수 최적화 방법 중 하나로 함수의 Local minimum을 찾는 방법

미분을 활용하여 함수가 가장 가파르게 증가하는 부분(기울기)에 음수를 취해 가장 가파르게 감소하는 부분으로 조금씩 이동시켜 주면서 함수가 극소가 되는 x를 찾는 방법입니다.

국소 최적해의 한계가 있지만 최소화 문제에 효율적으로 사용할 수 있습니다.



## 2) Advanced Convolutional Neural Network

**CNN**

사진데이터를 평면화 시키는 과정에서 공간 정보가 손실될 수 밖에 없는 한계를 극복하기 위해 이미지의 특징을 추출하는 부분과 클래스를 구분하여 이미지의 공간 정보를 유지한 상태로 학습이 가능한 모델

기본 용어 설명

Convolution: 2차원 입력데이터를 1개의 필터로 만들어 주기 위한 합성곱 연산

Filter: 이미지의 특징을 찾아내기 위한 공용 파라미터, 입력 데이터를 지정된 가격으로 순회하며 합성곱을 함

Stride: 필터를 순회하는 간격

Padding: Convolution Layer의 출력 데이터가 줄어드는 것을 방지하기 위한 방법. 입력 데이터의 외각에 지정된 픽셀만큼 특정 값을 채워 넣는 것

Pooling Layer: Convolution Layer의 출력 데이터를 입력으로 받아서 출력 데이터의 크기를 줄이거나 강조하는 용도로 사용함.

즉, CNN은 Filter의 크기, Stride, Padding과 Pooling 크기로 출력 데이터 크기를 조절하고, 필터의 개수로 출력 데이터의 채널을 결정함

결론적으로 CNN는 더 작은 학습 파라미터로 더 높은 인식률을 제공하는 모델임.

**Advanced CNN**

기존의 CNN 모델은 어떤 filter를 쓸 지 직접 수치를 수정하고 경험해보며 알 수 있었는데, 기존 CNN의 필터의 결과를 합치는 Inception Module을 만들어 이어 붙인 후 보다 더 의미 있는 결과 값을 찾을 수 있게 해주는 모델입니다.
"""

# 1) Gradient Descent 구현 하기

import torch 
from torch.autograd import Variable

x_data = [1.0, 2.0, 3.0]
y_data = [3.0, 6.0, 9.0]

w = 1 # 임의의 값 지정

def forward(x): 
  return x * w # 기본 식

def loss(x,y): # loss 계산
  y_pred = forward(x)
  return (y_pred - y) * (y_pred - y) # 예측 값과 실제 값의 거리 차를 돌려줌

def gradient(x,y): 
  return 2 * x * (x * w - y) # gradient를 계산함

print("학습 전", "값 :", forward(4))

for epoch in range(15): # 학습 과정
  for x_val, y_val in zip(x_data, y_data):
    grad = gradient(x_val, y_val)
    
    w = w - 0.01 * grad # 가중치 업데이트
    
    print("\tgrad:", x_val, y_val, round(grad,2))
    l = loss(x_val, y_val)
   
  print("prograss:", epoch, "w = ", round(w,2), "loss = ", round(l,5))
  
 
print("학습완료", "값 :", forward(4)) # 학습 확인


# 2) Advanced Convolutional neural network 구현하기


import torch 
import torch.nn as nn # 딥러닝 모델에 필요한 모듈이 모아져있는 패키지
import torch.nn.functional as F # 함수의 input으로 반드시 연산되어야 하는 값을 받는 기능
import torch.optim as optim # 최적화 방법이 있는 패키지
from torchvision import datasets, transforms # torch에서 제공해주는 데이터셋 가져오기

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # gpu 사용 가능 확인
batch_size = 64

train_dataset = datasets.MNIST(root='./mnist_data/',train = True, transform = transforms.ToTensor(),download = True) # 학습용 데이터셋

test_dataset = datasets.MNIST(root='./mnist_data/',train = False, transform = transforms.ToTensor()) # 학습 정도를 테스트하기 위한 데이터셋

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)  # 학습 데이터를 받아오는 함수

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=False) # 테스트 데이터를 받아오는 함수

class InceptionModule(nn.Module): # 여러 필터의 결과를 합치기 위한 인셉션 모듈 구현, nn.Module 상속

  def __init__(self,in_channels): # 네트워크 계층 정의
    super(InceptionModule,self).__init__() 
    self.branch1x1 = nn.Conv2d(in_channels,16,kernel_size=1) # _1 : 연산을 줄이면서 한 레이어에서 더 깊은 논리 처리 가능
  
    self.branch5x5_1 = nn.Conv2d(in_channels,16,kernel_size=1) # _1 과 같은 기능 
    self.branch5x5_2 = nn.Conv2d(16,24,kernel_size=5,padding=2) # 16채널을 5X5의 24개 채널로 만듦, 패딩을 통해 결과값이 작아지는 것을 방지
  
    self.branch3x3_1 = nn.Conv2d(in_channels,16,kernel_size=1) # _1 과 같은 기능
    self.branch3x3_2 = nn.Conv2d(16,24,kernel_size=3,padding=1) # 16채널을 3X3의 24개 채널로 만듦, 패딩을 통해 결과값이 작아지는 것을 방지
    self.branch3x3_3 = nn.Conv2d(24,24,kernel_size=3,padding=1) # 24채널을 3X3의 24개 채널로 만듦, 패딩을 통해 결과값이 작아지는 것을 방지
  
    self.branch_pool = nn.Conv2d(in_channels,24,kernel_size=1) 

  def forward(self,x): # 하나의 x를 4개로 쪼개주기 위함
    
    branch1x1 = self.branch1x1(x) 
    
    branch5x5 = self.branch5x5_1(x) 
    branch5x5 = self.branch5x5_2(branch5x5) 
    
    branch3x3 = self.branch3x3_1(x) 
    branch3x3 = self.branch3x3_2(branch3x3) 
    branch3x3 = self.branch3x3_3(branch3x3) 
    
    branch_pool = F.avg_pool2d(x,kernel_size=3,stride=1,padding=1) 
    branch_pool = self.branch_pool(branch_pool) 
    
    outputs = [branch1x1,branch5x5,branch3x3,branch_pool]
    return torch.cat(outputs, 1) # 4개의 함수를 하나로 합쳐준다. 채널의 개수는 총 88개(16+24+24+24)
  
  
  
class MainNet(nn.Module): # 전체 모델 구성
  def __init__(self): 
    super(MainNet,self).__init__() 
    self.conv1 = nn.Conv2d(1,10,kernel_size=5)  # 5x5의 Conv layer 10채널 통과
    
    self.conv2 = nn.Conv2d(88,20,kernel_size=5) # # 5x5의 Conv layer 20채널 통과, 인셉션 모델의 채널의 개수가 총 88개 이기 때문에 채널을 88개로 함
    
    self.incept1 = InceptionModule(in_channels=10) # 인셉션 모듈 통과
    self.incept2 = InceptionModule(in_channels=20) # 인셉션 모듈 통과
    
    self.max_pool = nn.MaxPool2d(2)  # 주어진 필터 범위 내에서 최대값을 뽑아내는 과정
    self.fc = nn.Linear(1408,10) # 마지막 Conv layer의 cell을 한줄로 나열한 후 그 개수에 맞추어 Fully connected layer의 input으로 넘겨주는 것, 즉, 1408개의 데이터를 10개로 바꿈

  def forward(self,x): 
    in_size = x.size(0) # size(0)을 하면 (n, 28*28)중 n을 리턴함 
    x = F.relu(self.max_pool(self.conv1(x))) # 학습을 위한 활성화 함수 relu
    x = self.incept1(x) 
    x = F.relu(self.max_pool(self.conv2(x))) 
    x = self.incept2(x) 
    x = x.view(in_size,-1) 
    x = self.fc(x) 
    return F.log_softmax(x) # 아웃풋을 한번에 묶어 결과를 조정해주기 위한 소프트맥스 함수 사용

model = MainNet().to(device) # 모델 정의
optimizer = optim.SGD(model.parameters(),lr=0.01,momentum=0.5) # 가중치를 업데이트 시켜주는 최적화 (Stochastic Gradient Descent) 사용, 과도한 연산 방지
#Stochastice Gradient Descent: 경사 하강법의 방법 중 하나로 기존의 경사하강법과 달리 전체 데이터를 계산하지 않고 일부 데이터를 계산하여 빠르게 연산을 해줌
criterion = nn.NLLLoss() # loss 함수 정의, softmax함수를 사전에 사용했기 때문에, NLLLoss를 사용합니다.

def train(epoch): 
  model.train() 
  for batch_idx, (data, target) in enumerate(train_loader): 
    data = data.to(device) 
    target = target.to(device) 
    
    output = model(data) # 데이터를 학습 모델에 투입
    
    optimizer.zero_grad() # gradient buffers를 0으로
    loss = criterion(output, target) # loss 계산
    loss.backward()  # 역전파 과정을 통해 각 변수마다 loss에 대한 gradient를 구해줌
    optimizer.step() # model의 파라미터들을 업데이트 해주는 함수
    if batch_idx % 50 == 0:
      print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(epoch, batch_idx * len(data), len(train_loader.dataset), 100. * batch_idx / len(train_loader), loss.data))

#batch: 전체 데이터를 나눠 일부를 묶은 것을 의미함
#epoch: 모든 학습 데이터에 대해 forward 와 backward pass를 한번 진행한 상태

def test(): # 과학습 가능성을 고려하여 별도의 테스트 함수 선언
  model.eval() 
  test_loss = 0 
  correct = 0 
  for data, target in test_loader: # 테스트 데이터 사용
    data = data.to(device) 
    target = target.to(device) 
    output = model(data) 
    test_loss += criterion(output, target).data # loss 계산
    pred = output.data.max(1, keepdim=True)[1] 
    correct += pred.eq(target.data.view_as(pred)).cpu().sum() #pred배열과 data의 일치 여부 검사해주는 기능
   
  test_loss /= len(test_loader.dataset)/batch_size 
  print('\nTest set: 평균 loss: {:.4f}, 정확도: {}/{} ({:.0f}%) \n'.format(test_loss, correct, len(test_loader.dataset), 100. * correct / len(test_loader.dataset)))
    
for epoch in range(1, 10): # 최종 실행
  train(epoch)
  test()