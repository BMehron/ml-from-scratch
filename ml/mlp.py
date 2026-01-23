# Manuall Implemenetation of Linear and re-LU layers
import torch 
import torch.nn as nn

class CustomLinear(nn.Module):
    def __init__(self, in_dim, out_dim):
        self.W = torch.zeros(out_dim, in_dim, requires_grad=True)
        self.b = torch.zeros(out_dim, requires_grad=True)

        self._randomly_initialize()

    def forward(self, input):
        return self.W@input.T + self.b
    
    def backward(self, input, out_grad):
        self.W.grad = out_grad@input.T
        self.b.grad = out_grad

    
class reLU(nn.Module):
    def forward(self, input):
        return input*(input >= 0)
    
    def backward(self, input, out_grad):
        return out_grad*(input >= 0)
