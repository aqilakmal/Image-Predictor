# ImagePredictor

Using Flask, I deploy a resnext101_32x8d model to predict uploaded images.

Dog
<p><img src="examples\ss\dog.jpg"></p>

Wallpaper
<p><img src="examples\ss\valley.jpg"></p>

Created an api that receive a POST request containing the image file to predict. The api returns a JSON array of the predictions with the appropriate labels and their respective confidence or percentages.

<p><img src="examples\ss\api.jpg"></p>