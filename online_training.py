import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import random
import os

class TransformerModel(nn.Module):
    def __init__(self, num_tokens, dim_model, num_heads, num_layers, dim_feedforward, dropout=0.1):
        super(TransformerModel, self).__init__()
        self.embedding = nn.Embedding(num_tokens, dim_model)
        self.positional_encoding = nn.Parameter(torch.zeros(1, 100, dim_model))
        self.transformer = nn.Transformer(dim_model, num_heads, num_layers, num_layers, dim_feedforward, dropout)
        self.fc_out = nn.Linear(dim_model, num_tokens)

    def forward(self, x):
        x = self.embedding(x) + self.positional_encoding[:, :x.size(1), :]
        x = self.transformer(x)
        x = self.fc_out(x[:, -1, :])
        return x
def load_csv_data(file_path):
    data = pd.read_csv(file_path)
    numbers = data['Number'].tolist()
    return numbers

# load csv file from csv_files folder

for file in os.listdir('csv_files'):

    csv_file = os.path.join('csv_files', file)
    numbers = load_csv_data(csv_file)

    # Hyperparameters
    num_tokens = 37  # Numbers between 0 and 36
    dim_model = 128
    num_heads = 8
    num_layers = 4
    dim_feedforward = 512
    learning_rate = 0.001

    # Initialize model, loss function, and optimizer
    model = TransformerModel(num_tokens, dim_model, num_heads, num_layers, dim_feedforward)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)


    def online_training_step(model, optimizer, criterion, sequence, target):
        model.train()
        optimizer.zero_grad()
        output = model(sequence.unsqueeze(0))  # Add batch dimension
        loss = criterion(output, target.unsqueeze(0))
        loss.backward()
        optimizer.step()
        return loss.item()

    def save_model(model, optimizer, epoch, path='model.pth'):
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, path)

    # Initialize a sequence for online learning
    sequence_length = 10  # Adjust based on your needs
    sequence = torch.tensor(numbers[:sequence_length])

    # Create a directory to save the models
    model_save_dir = 'saved_models'
    os.makedirs(model_save_dir, exist_ok=True)

    # Simulate online training with the CSV data
    for i in range(sequence_length, len(numbers)):
        new_number = numbers[i]
        target = sequence[-1]  # Last number as the target
        sequence = torch.cat((sequence[1:], torch.tensor([new_number])))  # Update sequence

        # Train model with the current sequence and target
        loss = online_training_step(model, optimizer, criterion, sequence[:-1], torch.tensor(target))
        print(f'Step {i + 1}, Loss: {loss}')

        # Save the model after each step
        model_save_path = os.path.join(model_save_dir, f'model_step_{i + 1}.pth')
        save_model(model, optimizer, i + 1, model_save_path)
