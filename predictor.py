import torch
import torchvision.transforms as transforms
import PIL.Image as Image

def predictImage(imgPath, best_only=True):
    '''
    Requires:
    torch
    torchvision.models as models
    torchvision.transforms as transforms
    PIL.Image as Image
    '''

    torch.device("cuda")
    model = torch.load("./predictor/resnext101_32x8d.pt")
    
    image = Image.open(imgPath)

    preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(244),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
        )
    ])

    img_pps = preprocess(image)
    batch_img_pps = torch.unsqueeze(img_pps, 0)
    model.eval()
    out = model(batch_img_pps)

    # Getting the labels
    with open('./predictor/imagenet_classes.txt') as f:
        labels = [line.strip() for line in f.readlines()]

    _, index = torch.max(out, 1)

    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

    if best_only:
        return (labels[index[0]], percentage[index[0]].item())
    else:
        _, indices = torch.sort(out, descending=True)
        return [(labels[i], percentage[i].item()) for i in indices[0][:5]]