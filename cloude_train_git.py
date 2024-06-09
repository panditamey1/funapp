import os
import torch
import torch.nn as nn
import pandas as pd
import math
from torch.utils.data import Dataset, DataLoader

# Roulette wheel layout and classes
WHEEL_LAYOUT = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
NUMBER_TO_POSITION = {num: idx for idx, num in enumerate(WHEEL_LAYOUT)}

ROULETTE_CLASSES = {
    "Big": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25],
    "Orph": [1, 20, 14, 31, 9, 17, 34, 6],
    "Small": [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33]
}

NUMBER_TO_CLASS = {num: cls for cls, nums in ROULETTE_CLASSES.items() for num in nums}
CLASS_TO_INDEX = {cls: idx for idx, cls in enumerate(ROULETTE_CLASSES.keys())}

class RouletteDataset(Dataset):
    def __init__(self, data, sequence_length):
        self.data = torch.tensor(data, dtype=torch.long)
        self.positions = torch.tensor([NUMBER_TO_POSITION[num] for num in data], dtype=torch.long)
        self.classes = torch.tensor([CLASS_TO_INDEX[NUMBER_TO_CLASS[num]] for num in data], dtype=torch.long)
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.data) - self.sequence_length

    def __getitem__(self, idx):
        x_nums = self.data[idx:idx + self.sequence_length]
        x_pos = self.positions[idx:idx + self.sequence_length]
        x_cls = self.classes[idx:idx + self.sequence_length]
        y_num = self.data[idx + self.sequence_length]
        y_pos = self.positions[idx + self.sequence_length]
        y_cls = self.classes[idx + self.sequence_length]
        return (x_nums, x_pos, x_cls), (y_num, y_pos, y_cls)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(0), :]

class RouletteTransformerModel(nn.Module):
    def __init__(self, num_classes, pos_classes, cls_classes, d_model, nhead, num_layers):
        super(RouletteTransformerModel, self).__init__()
        self.num_embedding = nn.Embedding(num_classes, d_model)
        self.pos_embedding = nn.Embedding(pos_classes, d_model)
        self.cls_embedding = nn.Embedding(cls_classes, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc_num = nn.Linear(d_model, num_classes)
        self.fc_pos = nn.Linear(d_model, pos_classes)
        self.fc_cls = nn.Linear(d_model, cls_classes)

    def forward(self, x):
        x_nums, x_pos, x_cls = x
        x = self.num_embedding(x_nums) + self.pos_embedding(x_pos) + self.cls_embedding(x_cls)
        x = self.pos_encoder(x)
        x = self.transformer_encoder(x)
        num_out = self.fc_num(x)
        pos_out = self.fc_pos(x)
        cls_out = self.fc_cls(x)
        return num_out, pos_out, cls_out

def train_on_file(model, file_path, sequence_length, batch_size, epochs, lr, device):
    print(f"Training on file: {file_path}")
    
    df = pd.read_csv(file_path)
    data = df["Number"].tolist()
    
    dataset = RouletteDataset(data, sequence_length)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for (batch_x_nums, batch_x_pos, batch_x_cls), (batch_y_nums, batch_y_pos, batch_y_cls) in train_loader:
            batch_x = (batch_x_nums.to(device), batch_x_pos.to(device), batch_x_cls.to(device))
            batch_y_nums, batch_y_pos, batch_y_cls = batch_y_nums.to(device), batch_y_pos.to(device), batch_y_cls.to(device)
            
            optimizer.zero_grad()
            num_out, pos_out, cls_out = model(batch_x)
            
            loss = criterion(num_out[:, -1], batch_y_nums) + criterion(pos_out[:, -1], batch_y_pos) + criterion(cls_out[:, -1], batch_y_cls)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Train Loss: {total_loss/len(train_loader):.4f}")

def predict_for_csv(model, csv_path, sequence_length, device):
    print(f"Predicting for file: {csv_path}")
    
    df = pd.read_csv(csv_path)
    data = df["Number"].tolist()
    
    predictions = []

    for i in range(len(data) - sequence_length):
        sequence = data[i:i + sequence_length]
        actual_next = data[i + sequence_length]
        
        with torch.no_grad():
            input_nums = torch.tensor(sequence, dtype=torch.long).unsqueeze(0).to(device)
            input_pos = torch.tensor([NUMBER_TO_POSITION[num] for num in sequence], dtype=torch.long).unsqueeze(0).to(device)
            input_cls = torch.tensor([CLASS_TO_INDEX[NUMBER_TO_CLASS[num]] for num in sequence], dtype=torch.long).unsqueeze(0).to(device)
            
            num_out, pos_out, cls_out = model((input_nums, input_pos, input_cls))
            
            predicted_num = torch.argmax(num_out[0, -1]).item()
            predicted_pos = WHEEL_LAYOUT[torch.argmax(pos_out[0, -1]).item()]
            predicted_cls = list(CLASS_TO_INDEX.keys())[torch.argmax(cls_out[0, -1]).item()]
            
            actual_cls = NUMBER_TO_CLASS[actual_next]
            
            predictions.append({
                "sequence": sequence,
                "actual_next": actual_next,
                "predicted_num": predicted_num,
                "num_correct": predicted_num == actual_next,
                "predicted_pos": predicted_pos,
                "pos_correct": predicted_pos == actual_next,
                "predicted_cls": predicted_cls,
                "actual_cls": actual_cls,
                "cls_correct": predicted_cls == actual_cls
            })
    
    pd.DataFrame(predictions).to_csv(f"predictions_{os.path.basename(csv_path)}", index=False)
    
    num_acc = sum(p["num_correct"] for p in predictions) / len(predictions) * 100
    pos_acc = sum(p["pos_correct"] for p in predictions) / len(predictions) * 100
    cls_acc = sum(p["cls_correct"] for p in predictions) / len(predictions) * 100
    
    print(f"Number Accuracy: {num_acc:.2f}%, Position Accuracy: {pos_acc:.2f}%, Class Accuracy: {cls_acc:.2f}%")

def main():
    # Hyperparameters
    d_model = 512
    nhead = 64
    num_layers = 8
    num_classes = 37  # 0 to 36
    pos_classes = len(WHEEL_LAYOUT)
    cls_classes = len(ROULETTE_CLASSES)
    sequence_length = 30
    batch_size = 64
    epochs = 50
    lr = 0.001

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize model
    model = RouletteTransformerModel(num_classes, pos_classes, cls_classes, d_model, nhead, num_layers).to(device)

    # Train on each CSV file
    data_folder = "csv_files"
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(data_folder, file)
            train_on_file(model, file_path, sequence_length, batch_size, epochs, lr, device)
            torch.save(model.state_dict(), f"roulette_predictor_{file[:-4]}.pth")

    # Predict for each CSV file
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(data_folder, file)
            predict_for_csv(model, file_path, sequence_length, device)

if __name__ == "__main__":
    main()