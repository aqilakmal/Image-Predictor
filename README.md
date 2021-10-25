# ImagePredictor

Using **Flask**, I deploy a resnet image classification model from the **torchvision** library to predict uploaded images.

**Dog**
<p><img src="examples\ss\dog.jpg"></p>

**Wallpaper**
<p><img src="examples\ss\valley.jpg"></p>

I created an api that receive a POST request containing the image file to predict. The api returns a JSON array of the predictions with the appropriate labels and their respective confidence or percentages.

<p><img src="examples\ss\api.jpg"></p>
