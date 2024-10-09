filename = 'images/porcupines/north-american-porcupine-erethizon-vintage-images.jpg';
RGB = imread(filename);
RGB2 = imresize(RGB, [200 200]);
s = size(RGB2);
imwrite(RGB2, filename);