%  Yiyun Wei
%  yiyunwei
%
% 16-311 Homework 0
% Hannah

function [ ] = p2(imageName)
% This function crops and then recolors an image.
% Input: imageName which is an image in .png format
% Output: topLeft.png (top 5x5 pixels of the original image)
% Output: stripes.png (striped version of the original image)

%% Set up

close all % closes previous figures
imageArray = imread(imageName); % reads in our image
imshow(imageArray); % shows this image

%% Crop

% INSERT YOUR CODE HERE FOR GETTING JUST THE TOP LEFT 5X5 PIXELS
% Don't forget to write this image to topleft.png
B = imageArray(1:5, 1:5);
imwrite(B, 'topleft.png')


%% Stripe

% INSERT YOUR CODE HERE FOR PUTTING BLACK STRIPES ON EVERY OTHER COLUMN
% Don't forget to write this image to stripes.png
C = imageArray;
for i=1:2:size(C,2)
    C(:,i,:) = 0;
end

imwrite(C, 'stripes.png')
