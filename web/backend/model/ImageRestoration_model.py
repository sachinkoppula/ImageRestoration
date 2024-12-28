import torch
import torch.nn as nn
import torch.nn.functional as F

class RestorationNet(nn.Module):
    def __init__(self, num_channels=64, num_blocks=16):
        super(RestorationNet, self).__init__()

        # Initial feature extraction
        self.conv_input = nn.Sequential(
            nn.Conv2d(3, num_channels, kernel_size=9, padding=4),
            nn.PReLU()
        )

        # Residual blocks
        self.residual_blocks = nn.ModuleList([
            nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1) for _ in range(num_blocks)
        ])

        # Upsampling
        self.upsampling = nn.Sequential(
            nn.Conv2d(num_channels, num_channels * 4, kernel_size=3, padding=1),
            nn.PixelShuffle(2),
            nn.PReLU(),
            nn.Conv2d(num_channels, num_channels * 4, kernel_size=3, padding=1),
            nn.PixelShuffle(2),
            nn.PReLU()
        )

        # Final reconstruction
        self.conv_output = nn.Conv2d(num_channels, 3, kernel_size=3, padding=1)

    def forward(self, x):
        feat = self.conv_input(x)
        for block in self.residual_blocks:
            feat = F.relu(block(feat)) + feat  # Skip connection (residual learning)

        out = self.upsampling(feat)
        out = self.conv_output(out)
        return torch.clamp(out, 0, 1)  # Clamp to valid image range [0, 1]
