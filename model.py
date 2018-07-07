"""
author: LeiLei
"""

import torch
import torchvision
from torch import nn
import torch.nn.functional as F
# 基于resnet34 hf_fcn  better hed
class HF_res34(nn.Module):
    def __init__(self,num_filters=32, pretrained=False,class_number=2):
        super().__init__()
        encoder = torchvision.models.resnet34(pretrained=pretrained)
        
        #start
        self.start=nn.Sequential(encoder.conv1,encoder.bn1,encoder.relu)#128*128
        self.d_convs=nn.Sequential(nn.Conv2d(num_filters*2,1,1,1),nn.ReLU(inplace=True))
        
        self.pool = nn.MaxPool2d(3,2,1)
        
        # layer1
        self.layer10=encoder.layer1[0]
        self.layer11=encoder.layer1[1]
        self.layer12=encoder.layer1[2]
        
        self.d_conv1=nn.Sequential(nn.Conv2d(num_filters*2,1,1,1),nn.ReLU(inplace=True))
        
        # layer2
        self.layer20=encoder.layer2[0]
        self.layer21=encoder.layer2[1]
        self.layer22=encoder.layer2[2]
        self.layer23=encoder.layer2[3]
        
        self.d_conv2=nn.Sequential(nn.Conv2d(num_filters*4,1,1,1),nn.ReLU(inplace=True))
        
        # layer3
        self.layer30=encoder.layer3[0]
        self.layer31=encoder.layer3[1]
        self.layer32=encoder.layer3[2]
        self.layer33=encoder.layer3[3]
        self.layer34=encoder.layer3[4]
        self.layer35=encoder.layer3[5]
        
        self.d_conv3=nn.Sequential(nn.Conv2d(num_filters*8,1,1,1),nn.ReLU(inplace=True))
        
        # layer4
        self.layer40=encoder.layer4[0]
        self.layer41=encoder.layer4[1]
        self.layer42=encoder.layer4[2]
        
        self.d_conv4=nn.Sequential(nn.Conv2d(num_filters*16,1,1,1),nn.ReLU(inplace=True))
        
        self.score=nn.Conv2d(17,class_number,1,1)# No relu loss_func has softmax
        
    def forward(self,x):
        input_size=x.shape[2:] # 可以获取 x的形状 那么采用 F.upsample
        
        x=self.start(x)
        s_x=self.d_convs(x)
        ss=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        ''' why no relu after upsample ? because before it , d_conv has relu '''
        x=self.pool(x)
        # layer1
        x=self.layer10(x)
        s_x=self.d_conv1(x)
        s10=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer11(x)
        s_x=self.d_conv1(x)
        s11=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer12(x)
        s_x=self.d_conv1(x)
        s12=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        
        # layer2
        x=self.layer20(x)
        s_x=self.d_conv2(x)
        s20=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer21(x)
        s_x=self.d_conv2(x)
        s21=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer22(x)
        s_x=self.d_conv2(x)
        s22=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer23(x)
        s_x=self.d_conv2(x)
        s23=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        
        # layer3
        x=self.layer30(x)
        s_x=self.d_conv3(x)
        s30=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer31(x)
        s_x=self.d_conv3(x)
        s31=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer32(x)
        s_x=self.d_conv3(x)
        s32=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer33(x)
        s_x=self.d_conv3(x)
        s33=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer34(x)
        s_x=self.d_conv3(x)
        s34=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer35(x)
        s_x=self.d_conv3(x)
        s35=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        
        # layer4
        x=self.layer40(x)
        s_x=self.d_conv4(x)
        s40=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer41(x)
        s_x=self.d_conv4(x)
        s41=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        x=self.layer42(x)
        s_x=self.d_conv4(x)
        s42=F.upsample(s_x,size=input_size,mode='bilinear',align_corners=True)
        
        cat=[ss,s10,s11,s12,\
             s20,s21,s22,s23,\
             s30,s31,s32,s33,s34,s35,\
             s40,s41,s42]
        # score
        score=self.score(torch.cat(cat,dim=1))
        
        return score
        
hed2=HF_res34()
print(hed2)
print(hed2.state_dict().keys()) 
